import React from 'react'
import OptionsClicker from './OptionsClicker'


const Text = ({entries, progress, langs, translate, translated, testMode, missingWordsObj, splitAnswer, setSplitAnswer,
   showOptions, setShowOptions, setAnswerSubmited, userAnswer, checkAnswer }) =>  {
  
    const handleShowMultiChoice = () => {
    setShowOptions(true)
    setSplitAnswer(entries[progress][langs[1]].split(' '))
  }

  const addSpecialChar = (e) => {
    userAnswer.current.value = userAnswer.current.value + e.target.value
  }

  return (
    <div className="generator-text-wrapper">
        <div className="actual-text">
        <span>{entries[progress][langs[0]]}</span>
    </div>
            
  {testMode ?
  <div>
    <div className="translation-words-with-input">
      {splitAnswer.map((word, i) => {
        
      if (word === missingWordsObj.word) {
        if (showOptions){
          return <OptionsClicker key={i} missingWordsObj={missingWordsObj} userAnswer={userAnswer}/>
        } else {
          return <div className="text-input-div" key={i}>
            <div>
            <button onClick={addSpecialChar} className="m-1 btn" value="č">č</button>
            <button onClick={addSpecialChar} className="m-1 btn" value="š">š</button>
            <button onClick={addSpecialChar} className="m-1 btn" value="ž">ž</button>
            </div>
            
            <input ref={userAnswer} type="text" placeholder="enter answer here" /></div>
        }} else {
        return <span key={i}>{word}</span>
      }
  })}
    </div>
    <div className="tranlation-buttons">
      <button className="btn btn-info" onClick={checkAnswer}>submit</button>
      {/* <button onClick={handleShowMultiChoice}>multiple choice</button> */}
    </div>
    
  </div>: 
  
  translated ? <div className="actual-text">
            {entries[progress][langs[1]]}
  </div>: <button className="btn translate-btn" onClick={translate}>click to translate</button>
  }                                                        
             
        </div>
       
  )
}


/*
// check multiword answer
function checkAnswer(input, answer){
  let correct = 0
  const length = answer.length
  answer.forEach((word, i) => {
    if (word === input[i]){
      correct++
    } 
  })
  if (length - correct < 2){
    return 'close!'
  } else {
    return 'wrong'
  }
}
*/
export default Text