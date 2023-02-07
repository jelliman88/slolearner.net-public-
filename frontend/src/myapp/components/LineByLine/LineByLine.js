import React from 'react'
import { useState, useEffect, useRef } from 'react'
import Line from './Line'


const LineByLine =({lessonEntries, langs, level, firstLang, websiteLang, lesson, format, actors, score, setScore, attemptedCount, 
  setAttemptedCount, setShowSummary, baseUrl, csrfToken, awsClipsBaseUrl}) => {
    const [entries, setEntries] = useState([])
    const homeworkAsString = document.getElementById('homework').textContent
    const homeworkArr = JSON.parse(homeworkAsString)
    
    useEffect(() => {
      lessonEntries.forEach(entry => {
        entry.show = false
      });
      setEntries(lessonEntries)
      }, [])

      const translateLine = (e) => {
        const { innerText, name } = e.target
        if (innerText === 'translate'){
          e.target.innerText = 'hide'
        } else {
          e.target.innerText = 'translate'
        }
        const index = parseInt(name)
        const updatedEntry = entries[index]
          if(updatedEntry.show){
          updatedEntry.show = false
          } else {
          updatedEntry.show = true
          }
          
          setEntries(prevState => [
          ...prevState.slice(0, index),
          updatedEntry,
          ...prevState.slice(index + 1, prevState.length)
      ])
    }
  return (
    <div className={format === 'dialogue' ? "lines dialogue-lines" : "lines"}>
        {entries.map((entry, i) => {
          return <Line key={i} index={i} entry={entry} level={level} langs={langs} translateLine={translateLine} firstLang={firstLang} websiteLang={websiteLang} lesson={lesson} 
           score={score} setScore={setScore} actors={actors} attemptedCount={attemptedCount} setAttemptedCount={setAttemptedCount}
           homeworkArr={homeworkArr} csrfToken={csrfToken} lessonLength={lessonEntries.length} setShowSummary={setShowSummary} baseUrl={baseUrl} awsClipsBaseUrl={awsClipsBaseUrl}/>
        })}

    </div>
  )
}

export default LineByLine