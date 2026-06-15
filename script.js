function updateClock() {
    const now = new Date();

    // Vaqt: HH:MM:SS
    let hours = now.getHours();
    let minutes = now.getMinutes();
    let seconds = now.getSeconds();

    // 24 soatlik format
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;

    const timeString = `${hours}:${minutes}:${seconds}`;

    // Sana: YYYY-MM-DD
    const year = now.getFullYear();
    const month = now.getMonth() + 1;
    const day = now.getDate();

    const monthFormatted = month < 10 ? '0' + month : month;
    const dayFormatted = day < 10 ? '0' + day : day;

    const dateString = `${year}-${monthFormatted}-${dayFormatted}`;

    // Hafta kuni (o'zbek tilida)
    const weekdays = ['Yakshanba', 'Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba'];
    const weekdayIndex = now.getDay();
    const dayName = weekdays[weekdayIndex];

    // HTML elementlarini yangilash
    document.getElementById('time').textContent = timeString;
    document.getElementById('date').textContent = dateString;
    document.getElementById('day').textContent = dayName;
}

// Soatni birinchi marta ko'rsatish
updateClock();

// Har 1 sekundda yangilash
setInterval(updateClock, 1000);