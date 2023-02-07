import React, { useState, useRef, useEffect } from 'react'
import Text from './Text'
import Progress from './Progress'
import FocusAndHomework from './FocusAndHomework';

const Generator = ({lessonEntries, lesson}) =>  {
    const homeworkAsString = document.getElementById('homework').textContent
    const homeworkArr = JSON.parse(homeworkAsString)
    const csrfToken = document.getElementById('csrf-token').value
    const engFlag = document.getElementById('eng-flag')
    const sloFlag = document.getElementById('slo-flag')
    const img = document.getElementById('lesson-image')
    engFlag.style.display = 'none'
    sloFlag.style.display = 'none'
    img.style.display = 'none'

    const [entries, setContext ] = useState(lessonEntries)
    const [progress, setProgress] = useState(0)
    const [langOrder, setLangOrder] = useState('eng slo')
    const [translated, setTranslated] = useState(false)
    const [boxBg, setBoxBg] = useState('')
    const [result, setResult] = useState('')
    const [focusMode, setFocusMode] = useState(false)
    const [focusProgress, setFocusProgress] = useState(0)
    const [alts, setAlts] = useState([])
    const [homeworkList, setHomeworkList] = useState(homeworkArr)
    const langs = langOrder.split(' ')
    const [modeSelected, setModeSelected] = useState(false)
    const [testMode, setTestMode] = useState(false)
    const missingWords = lesson.missing_words
    const missingWordsObj = missingWords[`${langs[1]}_data`][entries[progress].id]
    const [score, setScore] = useState([])
    const [splitAnswer, setSplitAnswer] = useState(entries[progress][langs[1]].split(' '))
    const [showOptions, setShowOptions] = useState(false)
    const [answerSubmited, setAnswerSubmited] = useState(false)
    const userAnswer = useRef()
    const actor = entries[progress].actor[lesson.id]

   
    
    const adjustProgress = (direction) => {
      if (direction == 'next'){
        setAnswerSubmited(false)
        if(focusMode){
          setFocusProgress(focusProgress + 1)
          setTranslated(false)
        } else {
          setProgress(progress + 1)
          setSplitAnswer(entries[progress + 1][langs[1]].split(' '))
          setTranslated(false)
          setBoxBg('')
      }} else { 
        
        if(focusMode){
          setFocusProgress(focusProgress - 1)
          setTranslated(false)
        } else {
          setAnswerSubmited(true)
          setTranslated(false)
          setProgress(progress - 1)
          setSplitAnswer(entries[progress - 1][langs[1]].split(' '))
          
        }
        
      }
      
      setShowOptions(false)
      userAnswer.current.value = ''
      setResult('')
    }
    const switchLang = () => {
      langOrder === 'eng slo' ? setLangOrder('slo eng'): setLangOrder('eng slo')
    }
  
    const focus = async () => {
      if(focusMode) {
        setFocusMode(false)
        setAlts([])
        setFocusProgress(0)
        setBoxBg('')
      } else {
        setFocusMode(true)
        setAlts(entries[progress].alts)
        setBoxBg('info')
      }
      
    }
  
    const translate = () => {
      setAnswerSubmited(true)
      setTranslated(true)
    }
  
    const homework = () => {
      const URL = 'http://127.0.0.1:8000/en/learn/add-remove-homework/'
      fetch(URL, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrfToken,
  
            
        },
        body: JSON.stringify({'id': entries[progress].id}) //JavaScript object of data to POST
    })
    .then(response => {
        return response.json() //Convert response to JSON
    })
    .then(data => {
        setHomeworkList(data)
    })}

    const handleModeSelect = (e) => {
      setModeSelected(true)
      const value = Boolean(e.target.value)
      setTestMode(value)
    }

    const checkAnswer = () => {
      setAnswerSubmited(true)
      const userInput = userAnswer.current.value
      const correctAnswer = missingWordsObj.word
      const res = gradeAnswer(userInput, correctAnswer)
      const borderColors = { '!': 'success', 'almost!': 'warning', 'wrong': 'danger'}
      setResult(res)
      setBoxBg(borderColors[res])
      }

    if (!modeSelected) {
      return (
        <div>
          <h3>pick a mode:</h3>
          <button onClick={handleModeSelect} value={true}>test</button>
          <button onClick={handleModeSelect} value="">practice</button>
        </div>
      )
    }
    return (
      
      <div className={"generator-wrapper border-" + boxBg }>
        <span className="actor">{actor !== 'none' ? actor: null}</span>
        <span className="result">{result}</span>
        <div className='switch-lang-box'>
          <img src={langs[0] === 'eng' ? engFlag.src: sloFlag.src} className="flag-icon" />
          <span onClick={switchLang} className="reverse-logo">↺</span>
          <img src={langs[0] === 'eng' ? sloFlag.src: engFlag.src} className="flag-icon" />
        </div>
        {!focusMode ?  
        <Text entries={entries} progress={progress} langs={langs} translate={translate} switchLang={switchLang} translated={translated}
         testMode={testMode} missingWordsObj={missingWordsObj} splitAnswer={splitAnswer} setSplitAnswer={setSplitAnswer}
        showOptions={showOptions} setShowOptions={setShowOptions}
        setAnswerSubmited={setAnswerSubmited} userAnswer={userAnswer} checkAnswer={checkAnswer}/>
        :
        <Text entries={alts} progress={focusProgress} langs={langs} translate={translate} switchLang={switchLang} translated={translated} />
        }                                                       
       <Progress entries={entries} focusMode={focusMode} adjustProgress={adjustProgress} focusProgress={focusProgress} 
        alts={alts} progress={progress} answerSubmited={answerSubmited} testMode={testMode} />
       
       <FocusAndHomework focus={focus} entries={entries} progress={progress} focusMode={focusMode} homework={homework} homeworkList={homeworkList} />
        </div>
    )
}


function gradeAnswer(userInput, correctAnswer){
  const input = prepareText(userInput)
  const answer = prepareText(correctAnswer)
  if (input === answer) {
    return 'correct!'
  } else {
    const splitInput = input.split(' ')
    const splitAnswer = answer.split(' ')
    const res = checkAOneWordAnswer(splitInput[0], splitAnswer[0])
    return res 
      } 
    }

function prepareText(text){
  const lower = text.toLowerCase()
  const trimmed = lower.trim()
  return trimmed
}

function checkAOneWordAnswer(input, answer){
  let correct = 0
  const length = answer.length
  let i = 0
  for(let char of answer){
    if (char === input[i]){
      correct++
    } 
    i++
  }
  if (length - correct < 2){
    return 'almost!'
  } else {
    return 'wrong'
  }
}


export default Generator


