import React, { useState, useEffect }  from 'react'
import MissingWord from './MissingWord'
import Alts from './Alts'
import HomeworkButton from '../helpers/HomeworkButton'
import AudioButton from '../helpers/AudioButton'

function timeout(delay) {
  return new Promise( res => setTimeout(res, delay) );
}


const Line = ({entry, level, langs, translateLine, index, firstLang, websiteLang, lesson, score, setScore,
  actors, attemptedCount, setAttemptedCount, homeworkArr, csrfToken,
  lessonLength, setShowSummary, baseUrl, awsClipsBaseUrl}) => {
  const [attempted, setAttempted] = useState(false)
  const [correct, setCorrect] = useState(false)
  const [showAlts, setShowAlts] = useState(false)
  const secondLang = firstLang === 0 ? 1 : 0
  const splitLine = entry[langs[secondLang]].split(' ')
  const [shuffledChoices, setShuffledChoices] = useState([])
  const missingWords = lesson.missing_words
  const missingWord = missingWords[`${langs[secondLang]}_data`][entry.id]
  const { options } = missingWord
  const choices = [...options, missingWord.word]
  const shuffled = choices.sort((a, b) => 0.5 - Math.random())
  let info = entry.info[level]
  if (!info){
    info = 'hello'
  }
  useEffect(()=> {
    // so that the multiple choices are shuffled only once, not on every change
    setShuffledChoices(shuffled)
  }, [])
 
  let dialogueSide
  if (entry.actor[lesson.id] === actors[0]){
    dialogueSide = 'left'
  } else {
    dialogueSide = 'right'
  }

  
  const handleSelect = async (e) => {
    
    const selected = e.target.value
    if (!attempted) {
      setAttemptedCount(attemptedCount + 1 > lessonLength ? attemptedCount: attemptedCount + 1)
    } 
    
    
    if (selected === missingWord.word) {
      setCorrect(true)
      if (!attempted){
        setScore(score + 1)
        }
    } else {
      setCorrect(false)
    }
    setAttempted(true)
    if (!attempted){
      if (attemptedCount + 1 === lessonLength ) {
        await timeout(1000)
        setShowSummary(true)
      }
    }
   
    // scroll ?
  }
  const handleShowAlts = () => {
      if (!showAlts){
        setShowAlts(true)
      } else {
        setShowAlts(false)
      }
  }
  return (
    <div className={lesson.type === 'dialogue' ? `line-wrapper ${dialogueSide}`: 'line-wrapper'}>
      
     <div className={lesson.type === 'dialogue' || 'news' ? attempted ? correct ? 'article-line border-success': 'article-line border-danger' : 'article-line ':
       attempted ? correct ? 'line border-success': 'line border-danger' : 'line' }>
        {/** line */}
      <div className="d-flex justify-content-start">
        <span className="info" title={info[langs[secondLang]]}>
          <span className={info[langs[secondLang]] ? "text-info h3": "invisible" } title={info[langs[secondLang]]}>&#9432;</span>
          <br />
          <span className={info[langs[secondLang]] ? "text-info": "invisible" }>info</span>
        </span>
        <span className="d-flex">
        <h4 >{entry[langs[firstLang]]}</h4>
        
        <h4><AudioButton file={firstLang === 0 ? entry.eng_audio: entry.slo_audio} csrfToken={csrfToken} awsClipsBaseUrl={awsClipsBaseUrl}/></h4>
        </span>
        <span className="homework-button-span"> <HomeworkButton status={homeworkArr.includes(entry.id) ? true: false} csrfToken={csrfToken} entryId={entry.id} baseUrl={baseUrl} helpText={firstLang === 0 ? 'homework' : 'domača naloga'}/></span>
       
       
        
      </div>
      <span onClick={handleShowAlts} className= {entry.alts[0] && attempted ? "focus-icon unselectable": "focus-icon hidden-text"}>{showAlts ?  websiteLang === 'en' ? 'hide' : 'skriti': websiteLang === 'en' ? 'focus' : 'fokus'}</span>
      
      
        {/** translated */}<h4 className={entry.show ? "highlight-text": "hidden-text"}> {splitLine.map((word, i) => { 
          if (word === missingWord.word){
            if (correct) {
              return <span key={i} className="revealed-missing-word border-bottom border-3 border-success">{word}</span>
            }
            return <MissingWord key={i} shuffledChoices={shuffledChoices} handleSelect={handleSelect}/>
          }
          return <span key={i}>{word} </span> 
          })}
          
          {correct ? <AudioButton file={firstLang === 0 ? entry.slo_audio: entry.eng_audio} csrfToken={{awsClipsBaseUrl}}  awsClipsBaseUrl={awsClipsBaseUrl}/>: null}
          
        </h4>
        <button className="btn btn-primary btn-sm button-width" name={index} onClick={translateLine}>{entry.show ? websiteLang === 'en' ? 'hide' : 'skriti': websiteLang === 'en' ? 'show' : 'pokazati'}</button>
        <div className="alts-wrapper">
        {showAlts ? 
        entry.alts.map((alt, i) => {
          return <Alts key={i} alt={alt} langs={langs} firstLang={firstLang} secondLang={secondLang} homeworkArr={homeworkArr} csrfToken={csrfToken} baseUrl={baseUrl} lesson={lesson}  websiteLang={websiteLang}/>
            
        }): null}
       
        </div>
       
      </div>
      
    <div>
        {/** <span className="line-counter">{ index + 1} {lesson.type === 'dialogue' ? currentActor: null }</span>*/}
        
      
      
      </div>
      
    </div>
  )
}

export default Line