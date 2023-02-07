import React, { useRef } from "react"

const Entry = ({ lesson, setEntries, index, entries, entry, handleAdd, alts, checkedEntry, setCheckedEntry, setResults, searchbarRef, setCheckedBox, actors, baseUrl}) => {
    //const updateValueRef = useRef()
    const keys = Object.keys(entry)
    
    const handleChange = (e) => {
        let { name, value } = e.target
        let updatedEntry = entries[index]
        updatedEntry[name] = value
        updatedEntry.id = 0
        setEntries(prevState => [
            ...prevState.slice(0, index),
            updatedEntry,
            ...prevState.slice(index + 1, prevState.length)
        ])
       
    }
    const handleDelete = (e) => {
        const index = parseInt(e.target.name)
        setEntries([
            ...entries.slice(0, index),
            ...entries.slice(index + 1, entries.length)
          ]);
    }

    const insertEntry = (index) => {
        const entry = checkedEntry
        setEntries(prevState => [
            ...prevState.slice(0, index),
            entry,
            ...prevState.slice(index + 1, prevState.length)
        ])
        setCheckedEntry({})
        setCheckedBox(null)
        //setResults([]) 
        searchbarRef.current.value = ''
    }
        return (
        <li className='entry-li'>

                <button onClick={() => insertEntry(index)} disabled={Object.keys(checkedEntry).length > 0 ? false: true} >insert</button>
                {lesson.type === 'dialogue' && !alts ? <select name="actor" onChange={handleChange} defaultValue={entry.actor}>
                {actors.map((actor, i) => {
                    return( <option key={i}>{actor}</option>)
                })}
                </select>: null}
                <input className="entry-text-input" type="text" value={entry.eng} name={keys[2]} onChange={handleChange} placeholder={keys[2]}/>
                <input className="entry-text-input" type="text" value={entry.slo} name={keys[3]} onChange={handleChange} placeholder={keys[3]}/>
                <button onClick={handleAdd} name={index}>add below</button>
                <button onClick={handleDelete} name={index}>delete</button>
                <a href={baseUrl + 'create/edit-entry/' + entry.id} >edit!</a>
            </li>
          )
    
   
  
}

export default Entry