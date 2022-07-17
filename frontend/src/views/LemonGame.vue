<template>
    <div>
        <Transition>
            <div class="message" v-if="message">
                {{ message }}
            </div>
        </Transition>
        <header>
            <h1> &#x1F52E Tarotble &#x1F0CF </h1>
        </header>
        <div>
            <div id="board-text">
                <input v-model="artist" placeholder="artist">
                <input v-model="track" placeholder="track">
                <div v-if="tarotReading==''">
                How can a song shape your day?
                <div v-if="tarotReading == ''">
                Input the song title and artist and read the resulting text. Read it again, read it a third time. How do you think it predicts the day? What intention can you set from it? Does it uncover a hope, a dream, a fear? Close your eyes, listen to your chosen song, and breathe.
                </div>
                We hope you have a ✨tarotble✨ day
                </div>  
                {{ tarotReading }}
            </div>
            <button v-if="!spinner" @click="fetchReading" class="button-1"> Enter Song </button>
            <button v-if="spinner" :disabled=true class="button-spinner"> Loading... </button>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import axios from 'axios';

@Component
export default class Tarotble extends Vue {
    private artist: string = '';
    private track: string = '';
    private tarotReading = '';
    private spinner: boolean = false;
    private message: string = '';

    private async fetchReading() {
        // call api with axios probably or something
        if (this.track === '' || this.artist === '') {
            this.showMessage('Both the artist and track names must be provided.');
            return
        }
        this.spinner = true;
        try {        
            let response = await axios.get('https://tarotble-r5rhqak6kq-uc.a.run.app/lyrics',
                                           {params: {track: this.track, artist: this.artist}});
            console.log(response);
            this.tarotReading = response['data']['data'];
            this.spinner = false;
        } catch (err) {
            console.log(err);
            this.showMessage(err['response']['data']['message']);
            this.spinner = false;
        }
        
    }
    private showMessage(msg: string, time = 2000) {
        this.message = msg;
        if (time > 0) {
            setTimeout(() => {
                this.message = '';
            }, time);
        }
    }
}

</script>


<style scoped>
#board-text {
    display: grid;
    grid-template-rows: repeat(4, 1fr);
    grid-gap: 5px;
    padding: 10px;
    box-sizing: border-box;
    --height: min(350px, calc(var(--vh, 100vh) - 310px));
    height: var(--height);
    width: min(350px, calc(var(--height) / 4 * 4));
    margin: 0px auto;
    white-space: normal;
    justify-content: center;
}
.center-text {
    white-space: normal;
    margin: 0px auto;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}
.message {
    position: absolute;
    left: 50%;
    top: 80px;
    color: #fff;
    background-color: rgba(0, 0, 0, 0.85);
    padding: 16px 20px;
    z-index: 2;
    border-radius: 4px;
    transform: translateX(-50%);
    transition: opacity 0.3s ease-out;
    font-weight: 600;
}
.message.v-leave-to {;
    opacity: 0;
}
.bolded { font-weight: bold; }
#board {
    display: grid;
    grid-template-rows: repeat(4, 1fr);
    grid-gap: 5px;
    padding: 10px;
    box-sizing: border-box;
    --height: min(350px, calc(var(--vh, 100vh) - 310px));
    height: var(--height);
    width: min(350px, calc(var(--height) / 4 * 4));
    margin: 0px auto;
}
.enter {
    --thing: min(420px, calc(var(--vh, 100vh) - 310px));
    width: min(350px, calc(var(--thing) / 4 * 4));
    height: min(105px, calc(var(--thing) / 4));
}
.row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-gap: 5px;
}
.tile {
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    font-size: 2rem;
    line-height: 2rem;
    font-weight: bold;
    vertical-align: middle;
    text-transform: uppercase;
    position: relative;
}
.correct {
    background-color: #75803e !important;
}

.present {
    background-color: #fcc219 !important;
}

.absent {
    background-color: #787c7e !important;
}
#answers {
    height: 174px;
}
h1 {
    margin: 4px 0;
    font-size: 36px;
}

header {
    border-bottom: 1px solid #ccc;
    margin-bottom: 30px;
    position: relative;
}
body {
    font-family: "Haas Grot Text R Web", "Helvetica Neue", Helvetica, Arial, sans-serif;
    text-align: center;
    max-width: 500px;
    margin: 0px auto;
}
.text {
    box-sizing: border-box;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    transition: transform 0.6s;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
}
@media (max-height: 680px) {
    .tile {
        font-size: 3vh;
    }
}
/* CSS */
.button-1 {
    background-color: #8f5cc4;
    border-radius: 8px;
    border-style: none;
    box-sizing: border-box;
    color: #FFFFFF;
    cursor: pointer;
    display: inline-block;
    font-family: "Haas Grot Text R Web", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 14px;
    font-weight: 500;
    height: 40px;
    --thing: min(350px, calc(var(--vh, 100vh) - 310px));
    width: min(350px, calc(var(--thing) / 4 * 4));
    line-height: 20px;
    list-style: none;
    margin: 0;
    outline: none;
    padding: 10px 16px;
    position: relative;
    text-align: center;
    text-decoration: none;
    transition: color 100ms;
    vertical-align: baseline;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}
.button-spinner {
    background-color: #e48beb;
    border-radius: 8px;
    border-style: none;
    box-sizing: border-box;
    color: #FFFFFF;
    cursor: wait;
    display: inline-block;
    font-family: "Haas Grot Text R Web", "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 14px;
    font-weight: 500;
    height: 40px;
    --thing: min(350px, calc(var(--vh, 100vh) - 310px));
    width: min(350px, calc(var(--thing) / 4 * 4));
    line-height: 20px;
    list-style: none;
    margin: 0;
    outline: none;
    padding: 10px 16px;
    position: relative;
    text-align: center;
    text-decoration: none;
    transition: color 100ms;
    vertical-align: baseline;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}
</style>
