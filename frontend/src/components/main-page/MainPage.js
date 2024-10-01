import React from 'react'
import Header from '../header/Header'
import Footer from '../footer/Footer'
import Card from '../card/Card'
import AddItemButton from '../add-item/AddItemButton'
import './style.css'

export default function MainPage() {
    return (
        <div>
            <Header />
            <div className='h-container'>
                <div className='box1'>
                    наверное выбор всякой всячины
                </div>
                <div className='box2'>
                    <Card label='картошка' description='омерзительная тварь (нет)' />
                    <AddItemButton />

                </div>
            </div>
            <Footer />
        </div>
    )
}
