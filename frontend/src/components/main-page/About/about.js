import React from 'react'
import StudentCard from './student-card/StudentCard'

const listStudents = {
  'Денис': {
    name: 'Денис',
    ico: '',
    link: 'https://github.com/Kseen715',
    des: 'Автоматизация технологических процессов сборки, настройка и развёртывание программного обеспечения.',
    subject: 'Девопс',
    image: process.env.PUBLIC_URL + '/students/Денис.png',
  },
  'Леонид': {
    name: 'Леонид',
    ico: '',
    link: 'https://github.com/o6ez9na',
    des: 'Разработка клиентской части веб-сайта.',
    subject: 'Фронтенд',
    image: process.env.PUBLIC_URL + '/students/Леонид.png',

  },
  'Анастасия': {
    name: 'Анастасия',
    ico: '',
    link: 'https://github.com/Nvnastya',
    des: 'Разработка серверной части веб-сайта.',
    subject: 'Бэкенд',  
    image: process.env.PUBLIC_URL + '/students/Анастасия.png',
  },
  'Николай': {
    name: 'Николай',
    ico: '',
    link: 'https://github.com/Kolan4ik2003',
    des: 'Тестировщик, разработка серверной части веб-сайта.',
    subject: 'Тесты',  
    image: process.env.PUBLIC_URL + '/students/Николай.png',

  },
  'Дарья': {
    name: 'Дарья',
    ico: '',
    link: 'https://github.com/kotikgriga27',
    des: 'Формализации спецификаций, архитектуры, функциональных требований и эксплуатационных инструкций для оптимизации разработки и эксплуатации программных систем; тестировщик.',
    subject: 'Дизайнер',
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