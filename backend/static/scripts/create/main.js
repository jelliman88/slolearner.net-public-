const lessonType = document.getElementById('lesson-type').value
console.log(lessonType)

function addEntryBelowClickedElm(clickedElm) {
    let position
    const list = document.querySelector('#entry-list')
    const entries = document.getElementsByClassName('entry-wrapper')
    clickedElm = clickedElm.children[0].value
    let i = 0
    for (let li of entries) {
    if (li.children[0].value === clickedElm){
        position = i
    }
    i++
}
    const li = createEntryLi()
    list.insertBefore(li, list.children[position + 1])
   
}
const createEntryLi = () => {
    const names = ['eng', 'slo']
    const div = document.createElement('div')
    div.classList.add('entry-wrapper')
    const li = document.createElement('li')
    
    names.forEach(name => {
        const input = document.createElement('input')
        if(name === 'eng'){
        input.classList.add('form-control', 'dropzone', name)
        } else {
          input.classList.add('form-control', name)
        }
       
        input.placeholder = name
        input.type = 'text'
        div.appendChild(input)
    })
    const entryControls = document.createElement('div')
    entryControls.classList.add('entry-controls')
    const addButton = document.createElement('button')
    addButton.innerHTML = '↓'
    addButton.type = 'button'
    addButton.setAttribute("onclick","addEntryBelowClickedElm(this.parentElement)");
    const deleteButton = document.createElement('button')
    deleteButton.innerHTML = 'x'
    deleteButton.setAttribute("onclick","removeEntry(this.parentElement.parentElement))")
    deleteButton.classList.add('btn','btn-danger','delete')
    entryControls.append( addButton, deleteButton)
    div.appendChild(entryControls)
    const select = createActorsSelectBox()
    li.append(select,div)
    li.classList.add('entry-li')
    
    return li
}

function createActorsSelectBox(){
  if(lessonType === 'dialogue'){ 
  const actors = [document.getElementById('actor-1').value, document.getElementById('actor-2').value]
  if (actors[0] != ''){
    const select = document.createElement('select')
    actors.forEach(actor => {
      const option = document.createElement('option')
      option.value = actor
      option.innerHTML = actor
      select.appendChild(option)
    })
    return select
  }
 else{
  return 'hello'
 }
}
else {

}
}



function onSave(){
    const form = document.querySelector('#entries-form')
    const lis = document.getElementsByClassName('entry-li')
    const actors = []
    const entryWrappers = []
    for (let li of lis){
      console.log(li.children)
      if (lessonType === 'dialogue'){
        actors.push(li.children[0].value)
      }
      entryWrappers.push(li.children[1])
    }
    
    const entriesList = []
    for (let [i, li] of entryWrappers.entries()){
      console.log(li)
      const doesEntryExist = li.id ? li.id: 'new-entry'
      const actor = lessonType === 'dialogue' ? actors[i]: null
  
        obj = { 
            eng: li.children[0].value,
            slo: li.children[1].value,
            id: doesEntryExist,
            actor: actor
          }
        entriesList.push(obj)
      
    }
    const entriesInput = document.querySelector('#entries-input')
    entriesInput.value = JSON.stringify(entriesList)
    form.submit()
    
}

function removeEntry(elm){
    const list = document.querySelector('#entry-list')
    list.removeChild(elm)

}

function clearInput(e){
    e.addEventListener("keydown", event => {
        if (event.keyCode === 46 || event.keyCode === 8) {
            document.getElementById('res-list').innerHTML = ''

        }
    
      });
}

function ajaxSearchEntry() {
  
    const entryQuery = document.getElementById('searchbar')
    const resList = document.getElementById('res-list')
    resList.innerHTML = ''
    const query = entryQuery.value
    if (query.length > 2){
        $.ajax({
            type: "POST",
            url: '/create/ajax-search-entry/',
            data: {
                search: query
            },
            dataType: 'json',
            success: function(data) {
                data.forEach((entry) => {
                 
                    const li = document.createElement('li')
                    const engSpan = document.createElement('span')
                    const sloSpan = document.createElement('span')
                    engSpan.innerHTML = entry.eng
                    sloSpan.innerHTML = entry.slo
                    li.append(engSpan, sloSpan) 
                    li.draggable = true
                    li.setAttribute("id",entry.id);
                    resList.appendChild(li)
                })
            }
        })
    }
   
}



// Drag and drop 
let dragged;


/* events fired on the draggable target */
document.addEventListener("drag", event => {
 
});

document.addEventListener("dragstart", event => {
  // store a ref. on the dragged elem
  dragged = event.target;

  // make it half transparent
  event.target.classList.add("dragging");
});

document.addEventListener("dragend", event => {
  // reset the transparency
  event.target.classList.remove("dragging");
});

/* events fired on the drop targets */
document.addEventListener("dragover", event => {
  // prevent default to allow drop
  event.preventDefault();
  
}, false);

document.addEventListener("dragenter", event => {
  // highlight potential drop target when the draggable element enters it
  if (event.target.classList.contains("dropzone")) {
    event.target.style.backgroundColor = 'orange'
    //event.target.classList.add("dragover");
  }
});

document.addEventListener("dragleave", event => {
  // reset background of potential drop target when the draggable element leaves it
  if (event.target.classList.contains("dropzone")) {
    event.target.style.backgroundColor = ''
    //event.target.classList.remove("dragover");
  }
});

document.addEventListener("drop", event => {
  // prevent default action (open as link for some elements)
  event.preventDefault();
  // move dragged element to the selected drop target
  if (event.target.classList.contains("dropzone")) {
    //event.target.classList.remove("dragover");
    //dragged.parentNode.removeChild(dragged);
    event.target.parentElement.id =  dragged.id
    event.target.value = dragged.children[0].innerHTML
    event.target.parentElement.children[1].value = dragged.children[1].innerHTML
    
  }
});

