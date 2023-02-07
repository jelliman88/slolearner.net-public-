import React from 'react'
import axiosPost from '../helpers/ajax'
import { useState } from 'react'



function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
const Searchbar = ({results, setResults, csrfToken, searchbarRef, checkedEntry, setCheckedEntry, checkedBox, setCheckedBox, baseUrl}) => {
    
    const handleChange = async (e) => {
        /* CODE SENDS TO SERVER EVERY KEY STROKE, SWITCHED TO BUTTON BUT WANT TO KEEP CODE JUST INCASE
         await delay(1000)
        const query = e.target.value
        const res = await axiosPost('create/ajax-search-entry/', csrfToken, {"query": query})
        setResults(res.data) 
        */
       
    }

    const handleClick = async () => {
        const query = searchbarRef.current.value
        if(query === ''){
            alert('enter a search word or phrase')
            return false
        }
        const res = await axiosPost(baseUrl,'create/ajax-search-entry/', csrfToken, {"query": query})
        if (res.data.length){
            setResults(res.data)
        } else {
            alert('no results')
        }  
    }

    const handleCheck = (entry, i) => {
        if(checkedBox === null){
            setCheckedBox(i)
            setCheckedEntry(entry)
        }else {
            setCheckedBox(null)
            setCheckedEntry({})
        }}
    const clearSearch = () => {
        setResults([])
        searchbarRef.current.value = ''

    }
  return (
    <div>
        <input ref={searchbarRef} type="text" placeholder='search database' onChange={handleChange}/>
        <button className='btn btn-warning m-1' onClick={handleClick}>go</button>
        <button className='btn' onClick={clearSearch}>clear</button>
        
        <div>
        
            <ul className='db-search-results'>
                {results.map((entry, i)=> {
                    return <li key={entry.id} className="results-li border p-1">
                        <span className='entrySpan'>{entry.eng}</span>
                        <span className='entrySpan'>{entry.slo}</span>
                        <input onChange={() => handleCheck(entry, i)} type="checkbox" checked={checkedBox != i? false: true } />
                    </li>
                })}
            </ul>
            
        
            
        </div>
    </div>
  )
}

export default Searchbar