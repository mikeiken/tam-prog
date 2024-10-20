import React from 'react'
import StudentCard from './student-card/StudentCard'

const listStudents = {
  'Денис': {
    name: 'Денис',
    ico: '',
    link: 'https://t.me/apateon',
    des: 'Автоматизация технологических процессов сборки, настройка и развёртывание программного обеспечения.',
    subject: 'Девопс',
    image: process.env.PUBLIC_URL + '/students/Денис.png',
  },
  'Леонид': {
    name: 'Леонид',
    ico: '',
    link: 'https://t.me/st4v3r',
    des: 'Разработка клиентской части веб-сайта.',
    subject: 'Фронтенд',
    image: process.env.PUBLIC_URL + '/students/Леонид.png',

  },
  'Анастасия': {
    name: 'Анастасия',
    ico: '',
    link: 'https://t.me/n_anastasya_v',
    des: 'Разработка серверной части веб-сайта.',
    subject: 'Бэкенд',  
    image: process.env.PUBLIC_URL + '/students/Анастасия.png',
  },
  'Николай': {
    name: 'Николай',
    ico: '',
    link: 'https://t.me/Kolan4ik_h',
    des: 'Тестировщик, разработка серверной части веб-сайта.',
    subject: 'Тесты',  
    image: process.env.PUBLIC_URL + '/students/Николай.png',

  },
  'Дарья': {
    name: 'Дарья',
    ico: '',
    link: 'https://t.me/koteikagrr_27',
    des: 'Формализации спецификаций, архитектуры, функциональных требований и эксплуатационных инструкций для оптимизации разработки и эксплуатации программных систем; тестировщик.',
    subject: '?????',  
    image: process.env.PUBLIC_URL + '/students/Дарья.png',
    
  }
};


export default function About() {
  return (
    <div className='about-wrapper centered-into-wrappers' style={{ '--font-size': '10em' }}>
      {Object.keys(listStudents).map((studentKey) => {
        const student = listStudents[studentKey];
        return (
          <StudentCard
            key={student.name}
            name={student.name}
            description={student.des}
            link={student.link}
            subject={student.subject}
            image={student.image}
          />
        );
      })}
    </div>
  );
}