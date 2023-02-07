import React, { useState } from 'react'

const OptionsClicker = ({missingWordsObj, userAnswer}) => {
  const { options, word } = missingWordsObj
  const missingWords = [...options, word]
  const shuffledWords = missingWords.sort((a, b) => 0.5 - Math.random());
  
  return (
    <select className="missing-words-wrapper" ref={userAnswer}>
      {shuffledWords.map((option,i) => {
        return <option key={i} value={option}>{option}</option>
      })}
      
    </select>
  
  )
}


export default OptionsClicker