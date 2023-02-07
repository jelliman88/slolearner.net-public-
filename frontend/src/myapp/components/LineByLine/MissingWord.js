import React, { useEffect } from 'react'

const MissingWord = ({ shuffledChoices, handleSelect }) => {
  return (
    <select className={'missing-word'} onChange={handleSelect}>
        <option hidden>?</option>
        {shuffledChoices.map((choice, i) => {
            return <option key={i}>{choice}</option>
        })}
    </select>
  )
}

export default MissingWord