import React from 'react'
import axios from 'axios';

const AudioButton = ({file, csrfToken, awsClipsBaseUrl}) => {
   
  const url = awsClipsBaseUrl + file
    const playAudio = async () => {
      const audio = new Audio(url)
      audio.play()
    }
  return (
    <i className="fa-solid fa-volume-high speaker-icon unselectable" onClick={playAudio}></i>
  )
}

export default AudioButton