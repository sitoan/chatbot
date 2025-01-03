import { Builder, By, Key, until, WebDriver } from "selenium-webdriver";

const testTourDetail = async () => {
  // Khởi tạo trình duyệt
  const driver: WebDriver = await new Builder().forBrowser("chrome").build();

  try {
    // Điều hướng đến trang web
    await driver.get("http://localhost:5173/tourdetail?id=1");

    // Kiểm tra tiêu đề trang
    // const header = await driver.findElement(By.id("header_banner")).getText();
    // console.log("Header banner:", header);

    // Kiểm tra thông tin giá
    const priceElement = await driver.findElement(
      By.xpath(
        "//div[contains(@class, 'textline')]/h5[text()='Price']/following-sibling::h5"
      )
    );
    const price = await priceElement.getText();
    console.log("Price of tour:", price);

    // Nhấn nút "Book now"
    const bookNowButton = await driver.findElement(By.id("book_now"));
    await bookNowButton.click();

    // Đợi modal hiện lên
    const modal = await driver.wait(
      until.elementLocated(By.className("modal")),
      5000
    );
    console.log("Modal is displayed:", await modal.isDisplayed());

    // Nhập số lượng người
    const slotsInput = await driver.findElement(By.id("slots"));
    await slotsInput.sendKeys("2", Key.RETURN);

    // Nhấn nút "Process"
    const processButton = await driver.findElement(By.id("payment_btn"));
    await processButton.click();

    // Đợi thông báo kết quả
    await driver.wait(until.alertIsPresent(), 5000);
    const alert = await driver.switchTo().alert();
    console.log("Alert message:", await alert.getText());
    await alert.accept();
  } catch (error) {
    console.error("Error during testing:", error);
  } finally {
    // Đóng trình duyệt
    await driver.quit();
  }
};

testTourDetail();
