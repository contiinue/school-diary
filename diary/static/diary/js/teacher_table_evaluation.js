let a = document.getElementById('table')

let storage

a.addEventListener('click', (elem) => {
  let td = elem.target.closest("td");
  if (!td) return;
  storage = elem.target.textContent || elem.target.value || ''
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
  let date = elem.target.parentElement.date_evaluation
  let pk = elem.target.parentElement.pk
  let student_id = elem.target.parentElement.parentElement.firstChild.student_id
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
  elem.target.parentElement.pk = json_parse.id
}

async function deleteEvaluation(pk) {
  let headers = getHeadets()
  await fetch(`http://127.0.0.1:8000/api/evaluation/${pk}`, {
    method: 'delete',
    headers: headers,
    })
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


function getHeadets() {
  let headers = new Headers();
  headers.append('X-CSRFToken', getCookie('csrftoken'))
  return headers
}

function getData(student_id, evaluation, date, update = false){
  let data = new FormData();
  data.append("evaluation", evaluation)
  data.append('date', converDate(date))
  if (!update) {
    data.append('student', student_id)
  }
  return data
}

function converDate (date) {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
} 


async function getDates() {
  // Get date of quarter for info blick table
  let some_dates = Array()
  let link = window.location.href.replace('?', '').split('/').slice(4)
  let r = await fetch(`http://127.0.0.1:8000/api/timetable/${link[0]}/${link[1]}?${link[2]}`)
  let response = await r.json()
  let info_first_elem = document.createElement('th')
  info_first_elem.innerHTML = '#'
  info_first_elem.classList.add('th_name_student', 'bg-light', 'info_th')
  some_dates.push(info_first_elem)

  for (let i of response.dates) {
    let date = new Date(i)
    elem = document.createElement('th')
    elem.classList.add('info_th')
    elem.innerHTML = date.getDate()
    elem.date = date
    some_dates.push(elem)
  }

  let avc = document.createElement('th')
  avc.innerHTML = 'Итоговая оценка'
  avc.classList.add('info_th', 'average_evaluation', 'bg-light')
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
  average_evaluation.classList.add('text-center', 'average_evaluation', 'bg-light')
  return average_evaluation
}

function getTdForTableStudents(student) {
  const fragment = Array();
  const td_info_block = Array.from(document.getElementById('info_block_for_evaluations').children).slice(1, -1)

  for (let elem of td_info_block) {
    let td = document.createElement('td')
    td.classList.add('td_evaluation')
    student.evaluation
    for (let eval of student.evaluation) {
      if (converDate(new Date(eval[2])) == converDate(elem.date)) {
        td.innerHTML = eval[1]
        td.pk = eval[0]
      }
    }
    td.date_evaluation = elem.date
    fragment.push(td)
}

  fio = document.createElement('th')
  fio.innerHTML = `${student.first_name} ${student.last_name}`
  fio.student_id = student.id
  fio.classList.add('th_name_student', 'bg-light')
  fragment.unshift(fio)

  fragment.push(getAverageEvaluation(fragment))
  return fragment
}

async function getStudents() {
  let link = window.location.href.replace('?', '').split('/').slice(4)
  let r = await fetch(`http://127.0.0.1:8000/api/evaluation/get_evaluations/?slug_name=${link[1]}&class_number=${link[0]}&${link[2]}`)
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
  for (let date of tr.children) {
    if (new Date() <= date.date) {
      a.firstElementChild.scrollLeft += date.offsetLeft
    }
  }
  
}

getTableOfEvaliations()
