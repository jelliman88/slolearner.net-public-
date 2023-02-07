import React from 'react'

const Progress = ({entries, focusMode, adjustProgress, focusProgress, alts, progress, answerSubmited, testMode }) => {
  
  return (
    <div className="generator-buttons-wrapper">
    { testMode ? null:  
    focusMode ? <button className="btn btn-warning" onClick={() => adjustProgress('back')} disabled={focusProgress === 0  ? true: false} >back</button> :
    <button className="btn btn-warning" onClick={() => adjustProgress('back')} disabled={progress === 0  ? true: false} >back</button>  }
   

    
    { focusMode ?  <button className="btn btn-success"onClick={() => adjustProgress('next')} disabled={focusProgress === alts.length -1 ? true: false}>next</button> : 
    progress === entries.length -1 ? <button className="btn btn-success"  disabled={answerSubmited ? false: true}>finish</button> :
   <button className="btn btn-success" onClick={() => adjustProgress('next')} disabled={answerSubmited ? false: true}>next</button> 
  }
     
   </div> 
  )
}

export default Progress