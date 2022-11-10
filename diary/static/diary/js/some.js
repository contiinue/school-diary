let a = document.getElementById('table')

let storage


a.addEventListener('click', (elem) => {
  let td = elem.target.closest("td");
  if (!td) return;
  storage = elem.target.innerHTML
  elem.target.innerHTML = ''

  let input = document.createElement('input')
  input.classList.add('input_evaluation')
  elem.target.append(input)
  elem.target.firstChild.focus()
})


a.addEventListener('input', (elem) => {
  if (elem.target.value.length === 1) {
    elem.target.innerHTML = elem.target.value
  }
  if (Number(elem.target.value) > 5 || Number(elem.target.value) <= 0 ) {
    elem.target.value = ''
  }
  else {
    elem.target.value = elem.target.value[0]
  }
})

a.addEventListener('mouseover', (elem) => {
  if (elem.target.tagName == 'TD') {
    elem.target.style.backgroundColor = '#e0e0e0'
  }
})

a.addEventListener('mouseout', (elem) => {
  elem.target.style.backgroundColor = ''
})

a.addEventListener('focusout', async (elem) => {
  
  if (!elem.target.value) {
    elem.target.parentElement.innerHTML = storage
    elem.target.remove()
    return
  }
  let date = elem.target.parentElement.getAttribute('date')
  let student_id = elem.target.parentElement.parentElement.children[0].getAttribute('student-id')
  elem.target.parentElement.innerHTML = elem.target.textContent
  setEvaluation(student_id, elem.target.textContent, date)
})

async function setEvaluation(student_id, evaluation, date) {
  let data = getData(student_id, evaluation, date)
  let headers = getHeadets()
  fetch('http://127.0.0.1:8000/api/evaluation/', {
    method: 'post',
    body: data,
    headers: headers,
    })
}

function getHeadets() {
  let headers = new Headers();
  let decodedCookie = decodeURIComponent(document.cookie);
  let csrf_token = decodedCookie.split(';')[0];
  headers.append('X-CSRFToken', csrf_token.split('=')[1]);
  return headers
}

function getData(student_id, evaluation, date){
  let data = new FormData();
  data.append("evaluation", evaluation)
  data.append('date', date)
  data.append('student', student_id)
  return data
}

async function changeEvaluation(pk) {
  let decodedCookie = decodeURIComponent(document.cookie);
  let ca = decodedCookie.split(';')[0];
  let data = new FormData();
  data.append("student", 4)
  data.append("evaluation", 2)
  data.append("quarter", 1)
  data.append('date', '2022-11-7')
  let headers = new Headers();
  headers.append('X-CSRFToken', ca.split('=')[1]);
  fetch(`http://127.0.0.1:8000/api/evaluation/`, {
      method: 'post',
      body: data,
      headers: headers,
})
 
}


function converDate (date) {
  return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}`
} 


async function getDates() {
  let some_dates = Array()
  let link = window.location.href.split('/').slice(4, 6)
  let r = await fetch(`http://127.0.0.1:8000/api/timetable/${link[0]}/${link[1]}/`)
  let response = await r.json()

  for (let i of response.dates) {
    let date_new = i.split()
    console.log(date_new)
    let date = new Date(i)
    elem = document.createElement('th')
    elem.innerHTML = date.getDate()
    elem.setAttribute('date', converDate(date))
    some_dates.push(elem)
  }

  let avc = document.createElement('th')
  avc.innerHTML = 'Итоговая оценка'
  some_dates.push(avc)

  return some_dates
}



function getTdForTableStudents(student) {
  const fragment = Array();
  const td_info_block = Array.from(document.getElementById('info_block_for_evaluations').children).slice(1, -1)


  for (let elem of td_info_block) {
    let element_date = elem.getAttribute('date')
    let td = document.createElement('td')
    td.classList.add('td_evaluation')
    td.setAttribute('date', element_date)
    
    if (student.evaluation) {
      for (let eval of student.evaluation) {
        let date_eval = converDate(new Date(eval[2]))
  
        if (date_eval == element_date) {
          td.setAttribute('pk', eval[0])
          td.innerHTML += eval[1]
        }
      }
    }
    fragment.push(td)

  if (td.textContent.length > 1) {
    
  }
}

  fio = document.createElement('th')
  fio.innerHTML = `${student.first_name} ${student.last_name}`
  fio.setAttribute('student-id', student.id)
  fragment.unshift(fio)


  return fragment
}

async function getStudents() {
  let link = window.location.href.split('/').slice(4, 6)
  let r = await fetch(`http://127.0.0.1:8000/api/evaluation/${link[0]}/${link[1]}/`)
  let students = await r.json()
  console.log(students)

  let td_students_evals = students.forEach((student) => {
    const fragment_tr = document.createDocumentFragment();
    
    const tr = document.createElement('tr')
    let td = getTdForTableStudents(student)
    
    for (let a of td) {
      tr.append(a)
    }
    fragment_tr.append(tr)
    const element  = document.getElementById('info_block_for_evaluations'); // assuming ul exists
    element.after(fragment_tr)
  })

}

async function getTableOfEvaliations() {
  let tr = document.getElementById('info_block_for_evaluations')
  let dates = await getDates()
  for (let elem of dates) {
    tr.append(elem) 
  }
  getStudents() 

}


getTableOfEvaliations()

