import React from 'react'
import Header from '../header/Header'
import Footer from '../footer/Footer'
import Card from '../card/Card'
import './style.css'

export default function MainPage() {
    return (
        <div>
            <Header />
            <div className='h-container'>
                <div className='box1'>
                    apgpapgna
                </div>
                <div className='box2'>
                    <Card />
                </div>
            </div>
            <Footer />
        </div>
    )
}
