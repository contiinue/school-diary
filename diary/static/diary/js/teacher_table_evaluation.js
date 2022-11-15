let a = document.getElementById('table')

let storage


a.addEventListener('click', (elem) => {
  let td = elem.target.closest("td");
  if (!td) return;
  storage = elem.target.textContent
  elem.target.innerHTML = ''

  let input = document.createElement('input')
  input.value = storage
  input.setAttribute('type', 'number')
  input.classList.add('input_evaluation')
  
  elem.target.append(input)
  elem.target.firstChild.focus()
})


a.addEventListener('input', (elem) => {
  let regexp = new RegExp(/[1-5]/g)
  if (elem.target.value.match(regexp)) {
    const evaluation = elem.target.value.match(regexp)
    elem.target.value = evaluation[1] || evaluation[0]
  }
})


a.addEventListener('focusout', async (elem) => {
  const childs = elem.target.parentElement.parentElement
  let date = elem.target.parentElement.getAttribute('date')
  let pk = elem.target.parentElement.getAttribute('pk')
  let student_id = elem.target.parentElement.parentElement.firstChild.getAttribute('student-id')

  if (!storage && elem.target.value && !pk) {
    await setEvaluation(student_id, elem.target.value, date, elem)
    elem.target.parentElement.textContent = elem.target.value
  } 
  else if (elem.target.value && elem.target.value != storage && storage) {
    elem.target.parentElement.textContent = elem.target.value
    await updateEvaluation(pk, elem.target.value, date)
    
  } 
  else if (!elem.target.value && storage) {
    await deleteEvaluation(pk)
    elem.target.remove()
  }
  else if (elem.target.value == storage) {
    elem.target.parentElement.innerHTML = storage
  }
  childs.lastChild.replaceWith(getAverageEvaluation(childs.children))
  storage = ''
})

async function updateEvaluation(pk, evaluation, date) {
  let data = getData(pk, evaluation, date, true)
  let headers = getHeadets()
  await fetch(`http://127.0.0.1:8000/api/evaluation/${pk}/`, {
    method: 'PUT',
    body: data,
    headers: headers,
    })
}


async function setEvaluation(student_id, evaluation, date, elem) {
  let data = getData(student_id, evaluation, date)
  let headers = getHeadets()
  let response = await fetch('http://127.0.0.1:8000/api/evaluation/set_evaluation/', {
    method: 'post',
    body: data,
    headers: headers,
    })
  let json_parse = await response.json()
  elem.target.parentElement.setAttribute('pk', json_parse.id)
}

async function deleteEvaluation(pk) {
  let headers = getHeadets()
  await fetch(`http://127.0.0.1:8000/api/evaluation/${pk}`, {
    method: 'delete',
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

function getData(student_id, evaluation, date, update = false){
  let old_date = date.split('-')
  let month = Number(old_date[1]) + 1
  let day = Number(old_date[2]) 
  let new_date = converDate(new Date(old_date[0], String(month), String(day)))
  let data = new FormData();
  data.append("evaluation", evaluation)
  data.append('date', new_date)
  if (!update) {
    data.append('student', student_id)
  }
  return data
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
    let date = new Date(i)
    elem = document.createElement('th')
    elem.classList.add('info_th')
    elem.innerHTML = date.getDate()
    elem.setAttribute('date', converDate(date))
    some_dates.push(elem)
  }

  let avc = document.createElement('th')
  avc.innerHTML = 'Итоговая оценка'
  avc.classList.add('info_th')
  some_dates.push(avc)

  return some_dates
}


function getAverageEvaluation (array_evaluations) {
  let summ = Number()
  let len = Number()
  for (let elem of array_evaluations) {
    if (elem.textContent && isNaN(elem.textContent) == false) {
      summ += Number(elem.textContent)
      len += 1
    }
  }
  let average_evaluation = document.createElement('th')
  const average = summ / len

  average_evaluation.innerHTML = isNaN(average) ?  0 : average.toFixed(2)
  average_evaluation.classList.add('text-center')
  return average_evaluation
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
}

  fio = document.createElement('th')
  fio.innerHTML = `${student.first_name} ${student.last_name}`
  fio.setAttribute('student-id', student.id)
  fragment.unshift(fio)

  fragment.push(getAverageEvaluation(fragment))
  return fragment
}

async function getStudents() {
  let link = window.location.href.split('/').slice(4, 6)
  let r = await fetch(`http://127.0.0.1:8000/api/evaluation/get_evaluations/?slug_name=${link[1]}&class_number=${link[0]}`)
  let students = await r.json()

  students.forEach((student) => {
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

let b = document.getElementById('sos')
b.pk = 1


console.log(document.getElementById('sos').pk)

getTableOfEvaliations()

