import "./main.css";
import LoginBtn from "../ui/login-btn/LoginBtn";
import RegisterBtn from "../ui/register-btn/RegisterBtn";

export default function LandingPage() {

    return (
        <>
            <header className="page-header">
                <div>TAMPROG</div>
                <div className={"buttons-wrapper"}>
                    <LoginBtn />
                    <RegisterBtn />
                </div>
            </header>
            <div className={"landing-main-wrapper"}>
                <div className={"section1"}>
                    <div className={"parallax-text"}>BSTUteam</div>
                </div>
                <div className={"section2"}>
                    <div className={"parallax-text"}>NORMAL</div>
                </div>
            </div>
        </>
    );
}