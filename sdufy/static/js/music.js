
let track_art = document.querySelector(".track-art");
let track_name = document.querySelector(".track-name");
let track_artist = document.querySelector(".track-artist");

let playpause_btn = document.querySelectorAll(".playpause-track")[0];
let next_btn = document.querySelector(".next-track");
let prev_btn = document.querySelector(".prev-track");

let seek_slider = document.querySelector(".seek_slider");
let volume_slider = document.querySelector(".volume_slider");
let curr_time = document.querySelector(".current-time");
let total_duration = document.querySelector(".total-duration");

let track_index = 0;
let isPlaying = false;
let updateTimer;

let curr_track = document.createElement("audio");


let track_list = []
function loadTrackList() {
  title = document.querySelectorAll('.musicTitle')
  artist = document.querySelectorAll('.musicArtist')
  image = document.querySelectorAll('.coverMusic')
  pathMusic = document.querySelectorAll('.pathMusic')
  for (let i = 0; i < title.length; i++) {
    let newTrack = {
      name : title[i].innerHTML,
      artist : artist[i].innerHTML,
      // image : (image[i].src).toString().replace('http://localhost:8000', ''),,
      image : "C:\\Users\\Lenovo\\Desktop\\project-final\\sdufy\\music\\2023-05-05_20-31-22.png",
      path :pathMusic[i].value
    }
    track_list.push(newTrack)
  }
}

let onlyOne = false
// function playCurrentMusic(pathMusic,musicTitle,musicArtist,coverMusic) {
//   track_list = []
//   onlyOne = true
//   track_list.push(
//       {
//         name : musicTitle,
//         artist : musicArtist,
//         image : coverMusic,
//         path : pathMusic
//       }
//   )
//   loadTrack(track_index);
//   if (!isPlaying) {
//     document.querySelectorAll('.playStop')[0].src= "/static/img/icon/play_btn.svg";
//     document.querySelectorAll('.playpause-track')[0].src= "/static/img/icon/play_btn.svg";
//     playTrack();
//   } else {
//     document.querySelectorAll('.playStop')[0].src= "/static/img/icon/pause.svg";
//     document.querySelectorAll('.playpause-track')[0].src= "/static/img/icon/pause.svg";
//     pauseTrack();
//   }
// }
loadTrackList()
alert(track_list)
function loadTrack(track_index) {

  clearInterval(updateTimer);
  resetValues();

  curr_track.src = track_list[track_index].path;
  curr_track.load();

  track_art.src =
    track_list[track_index].image;
  track_name.textContent = track_list[track_index].name;
  track_name.style.color  = "#fff"
  track_artist.textContent = track_list[track_index].artist;
  track_art.style.width = "30px";
  track_art.style.height = "30px";

  updateTimer = setInterval(seekUpdate, 1000);


  curr_track.addEventListener("ended", nextTrack);


  random_bg_color();
}
function resetValues() {
  curr_time.textContent = "00:00";
  total_duration.textContent = "00:00";
  seek_slider.value = 0;
}

function playpauseTrack() {
  if (!isPlaying) {
    console.log('isPlaying')
    document.querySelectorAll('.playStop')[0].src= "/static/img/icon/play_btn.svg";
    if (document.querySelectorAll('.playpause-track').length > 1)
    document.querySelectorAll('.playpause-track')[0].src= "/static/img/icon/play_btn.svg";
    playTrack();
  } else {
    document.querySelectorAll('.playStop')[0].src= "/static/img/icon/pause.svg";
    if (document.querySelectorAll('.playpause-track').length > 1)
    document.querySelectorAll('.playpause-track')[0].src= "/static/img/icon/pause.svg";
    pauseTrack();
  }

}

function playTrack() {
  curr_track.play();
  isPlaying = true;
}

function pauseTrack() {
  curr_track.pause();
  isPlaying = false;

}

function nextTrack() {
  if (track_index < track_list.length - 1) track_index += 1;
  else track_index = 0;
  loadTrack(track_index);
  playTrack();
}

function prevTrack() {

  if (track_index > 0) track_index -= 1;
  else track_index = track_list.length - 1;

  loadTrack(track_index);
  playTrack();
}

function seekTo() {
  seekto = curr_track.duration * (seek_slider.value / 100);
  curr_track.currentTime = seekto;
}

function setVolume() {
  curr_track.volume = volume_slider.value / 100;
}

function seekUpdate() {
  let seekPosition = 0;

  // Check if the current track duration is a legible number
  if (!isNaN(curr_track.duration)) {
    seekPosition = curr_track.currentTime * (100 / curr_track.duration);
    seek_slider.value = seekPosition;

    // Calculate the time left and the total duration
    let currentMinutes = Math.floor(curr_track.currentTime / 60);
    let currentSeconds = Math.floor(
      curr_track.currentTime - currentMinutes * 60
    );
    let durationMinutes = Math.floor(curr_track.duration / 60);
    let durationSeconds = Math.floor(
      curr_track.duration - durationMinutes * 60
    );

    // Add a zero to the single digit time values
    if (currentSeconds < 10) {
      currentSeconds = "0" + currentSeconds;
    }
    if (durationSeconds < 10) {
      durationSeconds = "0" + durationSeconds;
    }
    if (currentMinutes < 10) {
      currentMinutes = "0" + currentMinutes;
    }
    if (durationMinutes < 10) {
      durationMinutes = "0" + durationMinutes;
    }

    curr_time.textContent = currentMinutes + ":" + currentSeconds;
    total_duration.textContent = durationMinutes + ":" + durationSeconds;
  }
}

loadTrack(track_index);
