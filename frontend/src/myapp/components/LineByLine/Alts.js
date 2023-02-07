import React, { useState } from 'react'
import HomeworkButton from '../helpers/HomeworkButton'

const Alts = ({alt, langs, firstLang, secondLang, csrfToken, homeworkArr, baseUrl, lesson,  websiteLang}) => {
    const [translate, setTranslate] = useState(false)

    const handleTranslate = () => {
        if (translate){
            setTranslate(false)
        } else {
            setTranslate(true)
        }
    }
  
  return (
    <div className="alt">
    <div className="d-flex justify-content-evenly">
    <span className={!alt.info[toString(lesson.id)] ? 'invisible': null }>
          <span>&#9432;</span>
    </span>
    <span >{alt[langs[firstLang]]}</span>
    <HomeworkButton status={homeworkArr.includes(alt.id) ? true: false} csrfToken={csrfToken} entryId={alt.id} baseUrl={baseUrl}/>
    
    </div>
   
    <span className= { translate ? null: 'hidden-text'}>{alt[langs[secondLang]]}</span>
    <button onClick={handleTranslate} className="btn btn-primary btn-sm focus-show-hide-button">{translate ? websiteLang === 'en' ? 'hide' : 'skriti': websiteLang === 'en' ? 'show' : 'pokazati'}</button></div>
  )
}

export default Alts