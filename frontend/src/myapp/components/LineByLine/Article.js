import React, { useState } from 'react'
import LineByLine from './LineByLine'
import Summary from './Summary'
import axiosPost from '../helpers/ajax'

const Article = ({lessonEntries, lesson, format, lessons_in_order, baseUrl, csrfToken, awsClipsBaseUrl}) => {
    let bg
    const actors = lesson.actors.split('&')
    const [score, setScore] = useState(0)
    const [attemptedCount, setAttemptedCount] = useState(0)
    const nextLessonBaseHref = document.getElementById('next-lesson-base-href').value
    const user_first_lang = document.getElementById('first-lang').value
    const websiteLang = document.getElementById('website-lang').value
    const returnButton = document.getElementById('return-button')
    const level = returnButton.name
    const levelHref = returnButton.href
    if (format === 'news'){
        bg = document.getElementById('frontpage-bg')
        bg.style.display = 'none'
    } 
    //const img = document.getElementById('lesson-image')  for when making news articles
    //img.style.display = 'none'
    
    
    const langOrder = ('eng slo')
    const langs = langOrder.split(' ')
    const firstLang = langs.indexOf(user_first_lang)
    
    const [showSummary, setShowSummary] = useState(false)
    const [showLevelUp, setShowLevelUp] = useState(false)
    const [nextLevel, setNextLevel] = useState({})
    const [review, setReview] = useState(false)
    // show summary tiggers saving of progress, tried to put it in the summary component but was running too often
    if (showSummary){
        const adjustProgress = async () => {
        const res = await axiosPost(baseUrl,'learn/adjust-progress/', csrfToken, {"level": level, "lesson_id": lesson.id, 
        'score': score, 'lesson_len': attemptedCount})
        const levelUp = res.data.level_up
        if (levelUp === 'true'){
            setShowLevelUp(true)
            setNextLevel(res.data.next_level)
        }}
      adjustProgress()
    }

    const handleCloseSummary = () => {
        setShowSummary(false)
        setReview(true)
     }
    
     const typesTranslations = {'dialogue':'dialog','news': 'novice','verb': 'glagolnik','keywords': 'ključne besede'}
     lesson.slo_type = typesTranslations[lesson.type]
    return (
    <div className={format !== 'news' ? 'dialogue-wrapper': 'article-wrapper'}>
        
        <div className="line-by-line-bg" style={format === 'news' ? {backgroundImage: `url(${bg.src})`}: null}>
        {format === 'news' ? 
        <div className='topbox'>
         <div className={format === 'news' ? 'news-header' : 'format-header' }>{format === 'news' ? 'THE SLO LEARNER GAZETTE' : <h3>{format}</h3>}</div>
        </div>: null }
           
            <div className='lesson-top-bar'>
                <div className='type-title-description'>
                <span className='type text-danger'>{websiteLang === 'en' ? lesson.type : lesson.slo_type} - </span> 
                <span className='title'>{websiteLang === 'en' ? lesson.title : lesson.slo_title} - </span> 
                <span className='description text-info'>{websiteLang === 'en' ? lesson.description : lesson.slo_description}</span> 
                </div>
                
                <div className="d-flex justify-content-around">
                <a className="btn btn-danger m-1" href={levelHref}>{websiteLang === 'en' ? 'level ' : 'stopnja '}{level}</a>
                <a className="btn btn-light m-1" onClick={() => window.location.reload()}>{websiteLang === 'en'? 'restart' : 'ponovni zagon'}</a>
                <h5 disabled className={score === attemptedCount ? "btn btn-info m-1": "btn btn-warning m-1"}>{websiteLang === 'en' ? 'score' : 'rezultat'}: {score}/{attemptedCount}</h5> 
                </div>

            {/* <img className='image' src={img.src}/> */}
            </div>
                {format === 'dialogue' ? 
                 <div className="actors-header"><h1 className="p-1 rounded">{actors[0]}</h1> <h1 className="p-1 rounded">{actors[1]}</h1></div>:
                 null}

                 <LineByLine lesson={lesson} level={level} lessonEntries={lessonEntries} firstLang={firstLang} websiteLang={websiteLang} format={format} 
                langs={langs} actors={actors} score={score} setScore={setScore} attemptedCount={attemptedCount} setAttemptedCount={setAttemptedCount}
                setShowSummary={setShowSummary} baseUrl={baseUrl} csrfToken={csrfToken} awsClipsBaseUrl={awsClipsBaseUrl}/> 
                
            </div>
    
    <div className={showSummary && !review ? 'reveal' : 'hide'}>
    <Summary score={score} attempted={attemptedCount} levelHref={levelHref} level={level} lessons_in_order={lessons_in_order} baseUrl={baseUrl} 
    handleCloseSummary={handleCloseSummary} nextLessonBaseHref={nextLessonBaseHref} lesson={lesson} showLevelUp={showLevelUp} nextLevel={nextLevel} />
    </div>
    
        
    
    </div>
  )
}

export default Article

