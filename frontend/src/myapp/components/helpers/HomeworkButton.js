import React, { useState } from 'react'

const HomeworkButton = ({status, csrfToken, entryId, baseUrl, helpText}) => {
const [isOnList, setIsOnList] = useState(status)
const AddRemoveHomework = () => {
    
    const URL = baseUrl + 'learn/add-remove-homework/'
    fetch(URL, {
      method: 'POST',
      credentials: 'same-origin',
      headers:{
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
          'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({'id': entryId}) //JavaScript object of data to POST
  })
  .then(response => {

      return response.json() //Convert response to JSON
      
  })
  .then(data => {
    data.includes(entryId) ? setIsOnList(true): setIsOnList(false)
  })

}
  return (
    <span className="homework-add-remove-button" onClick={AddRemoveHomework} title={helpText}>
     { isOnList ?  <i className="fa-regular fa-square-check text-success"></i>: <i className="fa-regular fa-square-plus text-light"></i>}
     
    </span>
  )
}

export default HomeworkButton