import React from 'react'
import SearchBlock from './SearchBlock/SearchBlock';
import '../style.css'
import PlotInfo from './PlotInfo/PlotInfo';

export default function Garden() {
    return (
        <div className='content-container'>
            <SearchBlock />
            <PlotInfo />
        </div>
    )
}


