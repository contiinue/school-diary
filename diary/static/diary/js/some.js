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



a.addEventListener('focusout', async (elem) => {
  await changeEvaluation()
  if (!elem.target.value) {
    elem.target.parentElement.innerHTML = storage
    elem.target.remove()
    setTimeout(() => {
      elem.target.parentElement.style.backgroundColor = ''
    }, 1000);
    return
  }
  elem.target.parentElement.innerHTML = elem.target.textContent
  elem.target.remove()
})

async function changeEvaluation(pk) {
  alert(1)
  let r = await fetch(`http://127.0.0.1:8000/api/evaluation/${11}/`, {
    method: 'POST',
    body: {
      "id": 11,
      "student": 2,
      "evaluation": 5,
      "item": 1,
      "quarter": 1
  }
  })
}


function converDate (date) {
  return `${date.getFullYear()} ${date.getMonth()} ${date.getDate()}`
} 


async function getDates() {
  let some_dates = Array()
  let link = window.location.href.split('/').slice(4, 6)
  let r = await fetch(`http://127.0.0.1:8000/api/timetable/${link[0]}/${link[1]}/`)
  let response = await r.json()

  for (let i of response.dates) {
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

