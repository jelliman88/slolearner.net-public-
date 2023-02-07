import React from 'react'

const Summary = ({score, attempted, levelHref, level, lessons_in_order, handleCloseSummary, nextLessonBaseHref, lesson, showLevelUp, nextLevel}) => {
  const i = lessons_in_order.indexOf(lesson.id)
  const nextLevelUrl = levelHref.slice(0, - level.length)
  const nextLessonUrl = nextLessonBaseHref.slice(0, - String(lesson.id.length))
  const lastLessoninLevel = lessons_in_order[lessons_in_order.length - 1]
  return (
    <div className="summary border border-3 rounded border-info">
    <span className="x-button" onClick={handleCloseSummary}><i className="fa-solid fa-square-xmark"></i></span>
    <h5>lesson complete</h5>
    <div>you scored {score}/{attempted}</div>
    {showLevelUp ? 
    <span className="next-level-unlocked">
      <span><i className="fa-solid fa-lock-open"></i> next level unlocked</span>
      <a className="btn btn-success m-1" href={nextLevelUrl + nextLevel.level}>level {nextLevel.level} {nextLevel.title}</a>
    </span>
    :
    null}
    {lastLessoninLevel === lesson.id ? 
    null
    :
     score === attempted && level >  10 /* not until level does the next lesson button show up*/? <a className="btn btn-success m-1" href={nextLessonUrl + lessons_in_order[i + 1]}>next lesson</a> : null
    }
    <button className="btn btn-danger m-1" onClick={() => window.location.reload()}>try again</button>
    <a className="btn btn-info m-1" href={levelHref}>return to level {level} </a>
    
    </div>
  )
}

export default Summary