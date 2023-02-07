import React from 'react'

const FocusAndHomework = ({focus, entries, progress, focusMode, homework, homeworkList}) => {
  return (
    <div className="generator-extra-buttons-wrapper">
         <button onClick={focus} className="btn btn-pc5" disabled={entries[progress].alts.length > 0 ? false: true}>{focusMode ? 'return to lesson':  'focus mode' }</button>
         <button onClick={homework} className="btn btn-pc6">
         { homeworkList.includes(entries[progress].id) ? 'remove from homework': 'add to homework'
         }
         </button>
        </div>
  )
}

export default FocusAndHomework