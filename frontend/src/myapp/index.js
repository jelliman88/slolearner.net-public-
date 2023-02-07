import React from "react"
import { StrictMode, useState, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import Generator from './components/generator/Generator'
import Article from "./components/LineByLine/Article"
import Create from './components/Create/Create'
import Spinner from "./components/helpers/Spinner"
import FlashCardBox from "./components/Flashcards/FlashCardBox"
 
const App = () => {
  
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    setTimeout(() => setLoading(false), 500)
  }, [])
  function extract(id){
    
    let context = document.getElementById(id).textContent
    context = context.replace(/'/g, '"')
    context = context.slice(1,-1)
    if(id !== 'format'){
        try {
          context = JSON.parse(context)  
        } catch (error) {
          console.log(id)
          console.log(error)
        }
  }
    if (loading){
      return <Spinner/>
    }
    return context
  }
  // attain data
  let lessons_in_order
  const format = extract('format')
  const create = extract('create')
  const alts = extract('alts')
  const altEntry = extract('altEntry')
  let lessonEntries = extract('entries')
  const csrfToken = document.getElementById('csrf-token').value
  const baseUrl = document.getElementById('base-url').value
  const awsClipsBaseUrl = document.getElementById('aws_clips_base_url').value
  const lesson = extract('lesson')  
  if (!create) {
    lessons_in_order = extract('lessons_in_order') 
  }
  if (!lessonEntries){
    if(alts){
     let altEntries = extract('altsArr')
     lessonEntries = !altEntries ? []: altEntries
    } else {
      lessonEntries = []
    }
  }
  if (loading){
    return <Spinner/>
  }
  
  if (create){
      return (
        
        <Create lesson={lesson} lessonEntries={lessonEntries} alts={alts} altEntry={altEntry} csrfToken={csrfToken} baseUrl={baseUrl} />
        )
    }
    // sort dialogue here, background image and style 
  
  if (format !== 'generator'){
  return(
        <Article lessonEntries={lessonEntries} lesson={lesson} format={format} lessons_in_order={lessons_in_order}
         csrfToken={csrfToken} baseUrl={baseUrl} awsClipsBaseUrl={awsClipsBaseUrl}/>
      )
  }
    return(
      <Generator lessonEntries={lessonEntries} lesson={lesson} />
    )
    
  }


  // Mount the app to the mount point.
  const rootElement = document.getElementById('app')
  const root = createRoot(rootElement)

  root.render(
    <StrictMode>
      <App />
    </StrictMode>,
  );
  //ReactDOM.render(React.createElement(App, null, null), root)