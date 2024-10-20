import React from 'react';
import './student.css';

export default function StudentCard(props) {
  return (
    <div className='student-wrapper'>
        <img className='student-img' src={props.image} alt={props.name} />
        <div className='student-description'>
            <h2>
                <a className='student-link' href={props.link}>{props.name}</a> ({props.subject})
            </h2>
            <p className='description-fix-pos'>{props.description}</p>
        </div>
    </div>
  );
}
