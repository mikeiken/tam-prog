import React, {useState, useEffect} from "react";

export default function PlotInfoWindow({item}) {
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        if (item) {
            setIsVisible(true);
        } else {
            setIsVisible(false);
        }
    }, [item]);

    return (
        <div className={`container-plot-wrapper ${isVisible ? "visible" : ""}`}>
            <div className="container-plot-info">
                <div className={"container-wrapper-info"}>
                    <div className={"container-wrapper-img"}>
                        <img
                            className="plot-card-img"
                            src="https://avatars.mds.yandex.net/i?id=b4560f26cb2f9fab2f7395b28c1fed50_l-5236855-images-thumbs&n=13"
                            alt="img"
                        ></img>
                    </div>
                    <div className={"container-for-text"}>
                        <h3>Лучшее решение для начинающего предпринимателя!</h3>
                        <ul>
                            <li>
                                Минимальные обязательства
                            </li>
                            <li>
                                Простое обслуживание
                            </li>
                            <li>
                                Идеально для сезонного использования
                            </li>
                            <li>
                                Цена: {item.price}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

            <div className="container-plot-products">
                <h1>ID: {item.id}</h1>
            </div>
        </div>
    );
}
