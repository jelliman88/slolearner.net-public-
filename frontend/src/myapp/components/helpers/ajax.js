import axios from 'axios'
//const baseurl = 'https://slolearner.eu.pythonanywhere.com/en/'
//const baseurl = 'http://127.0.0.1:8000/en/'

const axiosPost = async (baseUrl,url,csrfToken, obj) => {
    const res = await axios({
        method: 'post',
        url: `${baseUrl}${url}`,
        headers:{
            'Accept': 'application/json',
            "Access-Control-Allow-Origin": "*",
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrfToken,
      },
        data: JSON.stringify(obj)
      })
    return res 
}
 



const ajaxPost = async (url,csrfToken, obj) => {
    const URL = `${baseurl}${url}`
await fetch(URL, {
  method: 'POST',
  credentials: 'same-origin',
  headers:{
      'Accept': 'application/json',
      'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
      'X-CSRFToken': csrfToken,
},
  body: JSON.stringify(obj) //JavaScript object of data to POST
})
.then(response => {
  return response.json() //Convert response to JSON
})
.then(data => {
  
    return data
})
}

export default axiosPost