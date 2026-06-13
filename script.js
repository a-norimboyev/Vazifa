// DOM elementlari
const hourHand = document.getElementById('hour-hand');
const minuteHand = document.getElementById('minute-hand');
const secondHand = document.getElementById('second-hand');
const digitalTimeElement = document.getElementById('digital-time');
const dateElement = document.getElementById('date');

// Soat vaqtini yangilovchi asosiy funksiya
function updateClock() {
    const now = new Date();
    
    // Vaqt komponentlari
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();
    let milliseconds = now.getMilliseconds();
    
    // Raqamli vaqtni formatlash (24 soatlik)
    const formattedHours = hours.toString().padStart(2, '0');
    const formattedMinutes = minutes.toString().padStart(2, '0');
    const formattedSeconds = seconds.toString().padStart(2, '0');
    digitalTimeElement.textContent = `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;
    
    // Sana formatlash (oy, kun, hafta kuni)
    const days = ['Yakshanba', 'Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba'];
    const months = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun', 'Iyul', 'Avgust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr'];
    
    const dayName = days[now.getDay()];
    const day = now.getDate();
    const month = months[now.getMonth()];
    const year = now.getFullYear();
    
    dateElement.textContent = `${dayName}, ${day} ${month} ${year}`;
    
    // --- MILLARNI BURCHAKLARI ---
    // Sekund mili: 360deg / 60 = 6deg/sekund, millisekundlar silliq harakat uchun
    const secondsDegrees = ((seconds + milliseconds / 1000) / 60) * 360;
    secondHand.style.transform = `translateX(-50%) rotate(${secondsDegrees}deg)`;
    
    // Minut mili: har daqiqa 6 gradus + sekundlar ta'siri (silliq harakat)
    const minutesDegrees = ((minutes + seconds / 60) / 60) * 360;
    minuteHand.style.transform = `translateX(-50%) rotate(${minutesDegrees}deg)`;
    
    // Soat mili: 12 soat = 360deg => 30deg/soat + minutlar ta'siri
    const hours24 = hours % 12;
    const hoursDegrees = ((hours24 + minutes / 60) / 12) * 360;
    hourHand.style.transform = `translateX(-50%) rotate(${hoursDegrees}deg)`;
}

// Soatga raqamlar va chiziqlarni dinamik qo'shish
function buildClockFace() {
    const numbersContainer = document.querySelector('.numbers');
    const ticksContainer = document.querySelector('.ticks');
    
    // 12 ta asosiy raqam (1 dan 12 gacha)
    for (let i = 1; i <= 12; i++) {
        const angle = (i * 30) - 90; // -90° chunki 12 yuqorida bo'lishi kerak (0° o'ng tomonga)
        const radian = angle * (Math.PI / 180);
        const radius = 135; // radius (soat yarmi - chegara)
        
        // Raqam div ini yaratish
        const numberDiv = document.createElement('div');
        numberDiv.classList.add('number');
        numberDiv.style.transform = `rotate(${angle}deg)`;
        
        const span = document.createElement('span');
        span.textContent = i;
        span.style.setProperty('--rot', angle);
        numberDiv.appendChild(span);
        numbersContainer.appendChild(numberDiv);
    }
    
    // Daqiqalik chiziqlar (60 ta chiziq - har bir minut)
    for (let i = 0; i < 60; i++) {
        const angle = (i * 6) - 90; // -90° boshlanish nuqtasi (12 yuqori)
        const tick = document.createElement('div');
        tick.classList.add('tick-mark');
        
        // Har 5-daqiqada (soat raqamlari yonida) qalinroq chiziq
        if (i % 5 === 0) {
            tick.classList.add('major');
        } else {
            tick.classList.add('minor');
        }
        
        tick.style.transform = `rotate(${angle}deg)`;
        ticksContainer.appendChild(tick);
    }
}

// Dastlabki yuklashda silliq ishlash va har soniyada yangilash
function init() {
    buildClockFace();   // Raqamlar va chiziqlarni yasash
    updateClock();      // Vaqtni darhol ko'rsatish
    
    // Har bir yangilanishda (har 20ms) mil silliq harakatlanishi uchun requestAnimationFrame
    // Lekin real vaqtda milni aniq ko'rsatish uchun setInterval emas, balki requstAnimationFrame mos keladi.
    // Ammo raqamli vaqtni 1 sek interval bilan o'zgartirish yetarli.
    // Milni har frame da yangilab, super silliq sekund mili uchun quyidagicha:
    
    function smoothLoop() {
        updateClock();
        requestAnimationFrame(smoothLoop);
    }
    requestAnimationFrame(smoothLoop);
    
    // Qo'shimcha: raqamli vaqt va sana har bir sekundda emas, balki millisekundda yangilanadi.
    // updateClock ichida hamma narsa tez-tez ishlaydi, bu zo'r.
}

// DOM to'liq yuklanganda ishga tushirish
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}