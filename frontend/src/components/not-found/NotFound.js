import React from 'react'

export default function NotFound() {
  return (
    <div className='not-found-container'>
      <div>
        <h1>404</h1>
        <p>Упс! Вы потерялись.
          <br />Мы искали эту страницу повсюду, но не смогли её найти.
          <br />Может, вернёмся на <a href='/'>главную</a> и попробуем ещё раз?</p>
      </div>
      <div>
        <img src={process.env.PUBLIC_URL + 'organic-food.png'} alt={'organic-food'} />
      </div>
    </div>
  )
}