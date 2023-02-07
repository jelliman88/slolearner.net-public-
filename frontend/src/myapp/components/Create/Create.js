import React from 'react'
import { useState, useEffect, useRef } from 'react'
import EntryList from './EntryList'
import Searchbar from './Searchbar'
import axiosPost from '../helpers/ajax'


const Create = ({lesson, lessonEntries, alts, altEntry, baseUrl, csrfToken}) => {
    const [entries, setEntries] = useState([])
    const [results, setResults] = useState([])
    const [checkedEntry, setCheckedEntry] = useState({})
    const searchbarRef = useRef()
    const [checkedBox, setCheckedBox] = useState(null)
    
    useEffect(() => {
        setEntries(lessonEntries)
        
    }, [])
    
    const handleSave = async () => {
      const entriesArr = entries
      entries.forEach(entry => {
        if(entry.id === 0){
          entry.eng = entry.eng.trim()
          entry.slo = entry.slo.trim() 
        }})
    
    const res =  await axiosPost(baseUrl,'create/ajax-save-entries/', csrfToken, {'entries': entriesArr, 'lesson':lesson,
     'alts': alts ? 'True': 'False', 'altEntry': alts ? altEntry: 'False'})
    alert(res.data)
    location.reload()

    }
    
  return (
    <div>
    <Searchbar csrfToken={csrfToken} checkedEntry={checkedEntry} setCheckedEntry={setCheckedEntry} results={results} 
    setResults={setResults} searchbarRef={searchbarRef} checkedBox={checkedBox} setCheckedBox={setCheckedBox} baseUrl={baseUrl}/>
    <EntryList entries={entries} lesson={lesson} setEntries={setEntries} alts={alts} checkedEntry={checkedEntry}
    searchbarRef={searchbarRef} setCheckedEntry={setCheckedEntry} setResults={setResults} handleSave={handleSave} setCheckedBox={setCheckedBox}
    baseUrl={baseUrl} />
    </div>
  )
}

export default Create