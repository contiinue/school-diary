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


a.addEventListener('focusout', (elem) => {
  if (!elem.target.value) {
    elem.target.parentElement.innerHTML = storage
    elem.target.remove()
    setTimeout(() => {
      elem.target.parentElement.style.backgroundColor = ''
    }, 1000);
    return
  }
  
  elem.target.parentElement.style.backgroundColor = 'green'
  elem.target.parentElement.innerHTML = elem.target.textContent
  elem.target.remove()
  setTimeout(() => {
    elem.target.parentElement.style.backgroundColor = 'red'
  }, 1000);
})

function converDate (date) {
  return `${date.getFullYear()} ${date.getMonth()} ${date.getDate()}`
} 


function getDates() {
  let some_dates = Array()
  for (let i = 1; i< 30; i++) {
    let a = 0 + i
    let date = new Date(2022, 10, a)
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

    for (let eval of student.evaluation) {
      let date_eval = converDate(new Date(eval[1]))

      if (date_eval == element_date) {
        td.innerHTML += eval[0]
      }
      fragment.push(td)
    }
  if (td.textContent.length > 1) {
    
  }

  }

  fio = document.createElement('td')
  fio.innerHTML = `${student.first_name} ${student.last_name}`
  fragment.unshift(fio)


  return fragment
}

async function getStudents() {
  let link = window.location.href.split('/').slice(4, 6)
  let r = await fetch(`http://127.0.0.1:8000/api/evaluation/${link[0]}/${link[1]}/`)
  let students = await r.json()

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

function getTableOfEvaliations() {
  let tr = document.getElementById('info_block_for_evaluations')
  let dates = getDates()
  for (let elem of dates) {
    tr.append(elem) 
  }
  getStudents() 

}


// const table = document.getElementById('table')

// let value 

// table.addEventListener('click', (elem) => {
//   let input = document.createElement('input')
//   let elem_valur = elem.target.value
//   elem.target.value = ''
  
//   input.classList.add('input_evaluation')
//   elem.target.append(input)
// })

// table.addEventListener('focusout', (elem) => {

// })


getTableOfEvaliations()

