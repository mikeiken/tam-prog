import React, { useState, useEffect } from "react";

export default function Welcome() {
  // Массив с приветствиями
  const greetings = [
    "Привет", // Русский
    "Hello", // Английский
    "Hola", // Испанский
    "Bonjour", // Французский
    "Ciao", // Итальянский
    "こんにちは", // Японский
    "안녕하세요", // Корейский
    "Hallo", // Немецкий
    "Olá", // Португальский
    "Nǐ hǎo", // Китайский
  ];

  const [greeting, setGreeting] = useState(greetings[0]);

  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);

    const interval = setInterval(() => {
      setIsVisible(false);
      setTimeout(() => {
        setGreeting((prevGreeting) => {
          const currentIndex = greetings.indexOf(prevGreeting);
          const nextIndex = (currentIndex + 1) % greetings.length;
          return greetings[nextIndex];
        });
        setIsVisible(true);
      }, 1000);
    }, 3000);

    return () => clearInterval(interval);
  }, []);
  return (
    <>
      <h1 className={isVisible ? "show" : ""}>{greeting}</h1>{" "}
    </>
  );
}
