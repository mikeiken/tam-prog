import React, { useState } from 'react';
import SearchBlock from './SearchBlock/SearchBlock';
import '../style.css';
import PlotInfo from './PlotInfo/PlotInfo';

export default function Garden() {
    const [selectedItem, setSelectedItem] = useState(null);

    return (
        <div className='content-container'>
            <SearchBlock onSelectItem={setSelectedItem} />
            <PlotInfo selectedItem={selectedItem} />
        </div>
    );
}
