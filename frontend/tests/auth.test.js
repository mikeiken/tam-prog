const { Builder, By, until, Capabilities } = require("selenium-webdriver");
const chrome = require("selenium-webdriver/chrome");
const assert = require("assert");

describe("Test axios with refresh token", function () {
  let driver;


  this.timeout(1500000);

  beforeEach(async () => {
    const options = new chrome.Options();
    options.addArguments("disable-web-security");
    options.addArguments("user-data-dir=/tmp/chrome-profile");

    driver = await new Builder()
      .forBrowser("chrome")
      .setChromeOptions(options)
      .build();
  });

  afterEach(async () => {
    await driver.quit();
  });

  it("should refresh token and make the request", async () => {
    // Мокируем данные в localStorage (перед каждым тестом)
    await driver.executeScript(() => {
      localStorage.setItem("accessToken", "initial-access-token");
      localStorage.setItem("refreshToken", "initial-refresh-token");
    });


    await driver.get("http://127.0.0.1:3000");

    // Обработка всех всплывающих окон (alert)
    try {
      await driver.wait(until.alertIsPresent(), 10000);  // Ждем появления alert
      let alert = await driver.switchTo().alert();  // Переключаемся на alert
      await alert.accept();  // Закрываем alert
      console.log("Alert closed successfully.");
    } catch (e) {
      console.log("No alert found, continuing with the test.");
    }

    // Время ожидания для загрузки страницы
    await driver.wait(until.titleIs("Your Page Title"), 90000);

    // Ожидания активации кнопки
    const button = await driver.wait(
      until.elementLocated(By.id("some-button")),
      90000
    );
    await driver.wait(until.elementIsVisible(button), 90000);  // Проверка видимости кнопки

    // Нажимаем на кнопку, которая вызывает axios запрос
    await button.click();

    // Ждем, пока результат обновится и элемент с ID "result" станет доступным
    await driver.wait(until.elementLocated(By.id("result")), 10000);

    // Проверяем, что данные отображаются корректно после обновления токенов
    const result = await driver.findElement(By.id("result")).getText();
    assert.strictEqual(result, "Success");

    // Проверяем, что в запросе используется новый токен
    const token = await driver.executeScript(() => {
      return localStorage.getItem("accessToken");
    });
    assert.strictEqual(token, "new-access-token");
  });
});
