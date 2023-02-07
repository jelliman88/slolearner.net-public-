import React from 'react'
import Entry from './Entry'

const EntryList = ({entries, lesson ,setEntries, alts, checkedEntry, setCheckedEntry, setResults, searchbarRef, handleSave, setCheckedBox, baseUrl}) => {
    const actors = lesson.actors.split("&")
    const handleAdd = (e) => {
        const index = parseInt(e.target.name)
        const newEntry = {
            id: 0,
            actor: actors[0],
            eng: "",
            slo: "",
            alts: {},
            
        } 
        setEntries(prevState => [
            ...prevState.slice(0, index +1),
            newEntry,
            ...prevState.slice(index + 1, prevState.length)
        ])
    }
    if (entries.length){
        return (
        <ol className='entries-ol'>
            <button className="btn btn-primary" onClick={handleSave}>save</button>
            {entries.map((entry,i) => {
                return ( 
                <Entry key={i} index={i} lesson={lesson} 
                setEntries={setEntries} entries={entries} 
                entry={entry} handleAdd={handleAdd} alts={alts}
                checkedEntry={checkedEntry} setCheckedEntry={setCheckedEntry} setResults={setResults}
                searchbarRef={searchbarRef} setCheckedBox={setCheckedBox} actors={actors} baseUrl={baseUrl}/>
                )})}
            </ol>
          )}
    else{
        return (
        <>
        <button className="btn btn-primary" name="0"onClick={handleAdd}>start</button>
        <button className="btn btn-primary" onClick={handleSave}>save</button> 
        </>
        )
    }
 
}

export default EntryList