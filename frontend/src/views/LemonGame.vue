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
        <div v-if="true">
            <div id="board-text">
               <!-- <p> woah coothingl: {{artist}} </p>
                     <p> woah again: {{track}} </p>
               -->
                <input v-model="artist" placeholder="artist">
                <input v-model="track" placeholder="track">
            </div>
            <button v-if="true" @click="callAubreyCode" class="button-1"> Enter Song </button>
        </div>

        <div v-if="False">
            <div id="board-text">
                What can you make from lemons? <br>
                <br>
                Form words using exactly all 16 letters. <br>
                Play for the best time or score over 3 rounds.<br>
                Share with your friends! <br>
                <br>
                3- and 4- letter words are 1 point each<br>
                5-letter words are 2 points each<br>
                6-letter words are 3 points each<br>
                7-letter words are 5 points each<br>
                8-letter words are 11 points each 
            </div>
            <button v-if="roundNumber < 4" @click="startGame" class="button-1"> I'm Ready! </button>
        </div>
        <div v-else-if="False">
            <div id="board-text">
                <div v-for="(round,i) in rounds">
                    Round {{round.roundNumber}}! Time: {{round.time}}, Score: {{score(round)}} <br>
                    <span v-for="(word, i) in round.solutionWords">
                        {{getSolution(word)}} ({{getSolutionScore(word)}})
                    </span>
                </div>
                <div v-if="roundNumber === 4">
                    Some other possible answers:
                    <div v-for="(round,i) in rounds">
                        {{roundText(i)}}
                    </div>
                </div>
            </div>
            <button v-if="roundNumber < 4" @click="startGame" class="button-1"> I'm Ready! </button>
            <button v-else-if="roundNumber === 4" @click="shareGame" class="button-1"> Share Results! </button>
        </div>
        <div v-else-if="False">
            <div> Round: {{roundNumber}} </div>
            <div > {{time}} </div>
            <div id="board">
                <div v-for="(lll, i) in letterStates" class="row">
                    <button v-for="(ll, j) in lll"
                            :disabled="ll.order === -2"
                            @click="setSolution(ll, j, i)"
                            class="tile"
                            :class="getStatus(ll.order, j, i)"
                    >
                        {{ll.letter}}
                    </button>
                </div>
            </div>
            <button v-if="!roundReady" class="button-1" @click="enterSolution"> Enter </button>
            <button v-if="roundReady && roundNumber < 3" class="button-1" @click="nextRound"> Next Round! </button>
            <button v-if="roundReady && roundNumber >= 3" class="button-1" @click="nextRound"> Continue! </button>
            <div id="answers">
                <button class="button-3" v-if="solution.length > 0" @click="removeSolution(solution, -1)">
                    {{getSolution(solution)}} ({{getSolutionScore(solution)}}) <b> X</b>
                </button>
                <button v-if="!roundReady" class="button-2" v-for="(word, index) in solutionWords"
                        @click="removeSolution(word, index)"
                        align="center"
                        justify="center"
                        :disabled="roundReady"
                > {{getSolution(word)}} ({{getSolutionScore(word)}}) <b>X </b> </button>
                <button v-if="roundReady" class="button-4" v-for="(word, index) in solutionWords"
                       @click="removeSolution(word, index)"
                        align="center"
                        justify="center"
                        :disabled="roundReady"
                > {{getSolution(word)}} ({{getSolutionScore(word)}})</button>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import dict from '!raw-loader!../assets/dict.txt';

interface LetterState {
    letter: string;
    order: number;
}

interface SolutionLetter {
    x: number;
    y: number;
    letter: string;
}

interface RoundData {
    roundNumber: number;
    solutionWords: SolutionLetter[][];
    status: string;
    startTime: Date;
    endTime: Date;
    time: string;
}

@Component
export default class LemonGame extends Vue {
    private artist: string = '';
    private track: string = '';
    private time: string =  '00:00:00.000';
    private gameStarted: boolean = false;
    private gameTimer: number = 0;
    private stoppedDuration: number = 0;
    private timeBegan: Date = null;
    private timeEnd: Date = null;
    private solution: SolutionLetter[] = [];
    private solutionWords: SolutionLetter[][] = [];
    private order: number = 0;
    private message: string = '';
    private lemonLetters1: string = 'SOURORANGECITRON';
    private lemonLetters2: string = 'TECHNICALLYBERRY';
    private lemonLetters3: string = 'SIXHUNDREDPOUNDS';
    private lemonPhrase1: string = 'SOUR ORANGE CITRON: Lemons are a hybrid between a sour orange and a citron.';
    private lemonPhrase2: string = 'TECHNICALLY BERRY: Lemons are berries in the botanical sense.';
    private lemonPhrase3: string = 'SIX HUNDRED POUNDS: Lemons trees can produce up to 600lbs of lemons every year.';
    private showModal: boolean = true;
    private letterStates: LetterState[][] = [];
    private rounds: RoundData[] = [];
    private roundNumber: number = 1;
    private dictSet: Set<string> = new Set<string>();
    private roundPause: boolean = false;
    private roundReady: boolean = false;
    private mounted(): void {
        for (const word of dict.match(/\b(\w+)\b/g)) {
            this.dictSet.add(word);
        }
    }
    private loadRound() {
        let letters: string = '';
        if (this.roundNumber === 1) {
            letters = this.lemonLetters1;
        } else if (this.roundNumber === 2) {
            letters = this.lemonLetters2;
        } else {
            letters = this.lemonLetters3;
        }

        this.letterStates = [];
        for (let i = 0; i < 4; i++) {
            const newLetters: LetterState[] = [];
            for (let j = 0; j < 4; j++) {
                const randomLetterPosition = Math.floor(Math.random() * letters.length);
                const ls: LetterState = {letter: letters[randomLetterPosition], order: -1 };
                letters = letters.slice(0, randomLetterPosition) + letters.slice(randomLetterPosition + 1);
                newLetters.push(ls);
            }
            this.letterStates.push(newLetters);
        }
        this.roundReady = false;
    }
    private callAubreyCode() {
        this.showMessage('Aubrey is cute ' + this.artist + ' ' + this.track);
        // call api with axios probably or something
    }
    private showMessage(msg: string, time = 1000) {
        this.message = msg;
        if (time > 0) {
            setTimeout(() => {
                this.message = '';
            }, time);
        }
    }
    private getSolution(sol: SolutionLetter[]): string {
        let solString: string = '';
        for (const sl of sol) {
            solString = solString + sl.letter;
        }
        return solString;
    }
    private getSolutionScore(sol: SolutionLetter[]): number {
        if (sol.length <= 4) {
            return 1;
        } else if (sol.length === 5) {
            return 2;
        } else if (sol.length === 6) {
            return 3;
        } else if (sol.length === 7) {
            return 5;
        } else {
            return 11;
        }
    }
    private score(round: RoundData): number {
        let roundScore: number = 0;
        for (const word of round.solutionWords) {
            roundScore = roundScore + this.getSolutionScore(word);
        }
        return roundScore;
    }
    private setSolution(ls: LetterState, x: number, y: number) {
        if (ls.order === -1) {
            const solLetter: SolutionLetter = {
                x,
                y,
                letter: ls.letter,
            };
            this.solution.push(solLetter);
            ls.order = this.order;
            this.order = 1;
        } else {
            this.solution = this.solution.filter((sl) => sl.x !== x || sl.y !== y);
            ls.order = -1;
        }
    }
    private roundText(roundNumber: number): string {
        let lemonPhrase: string = '';
        if (roundNumber === 0) {
            lemonPhrase = this.lemonPhrase1;
        } else if (roundNumber === 1) {
            lemonPhrase = this.lemonPhrase2;
        } else {
            lemonPhrase = this.lemonPhrase3;
        }
        return lemonPhrase;
    }
    private enterSolution() {
        if (this.solution.length < 3) {
            this.showMessage(`All words must be at least three letters long`);
            return;
        }
        if (this.dictSet.has(this.getSolution(this.solution))) {
            this.solutionWords.push(this.solution);
            this.solution = [];
            let won: boolean = true;
            for (const lll of this.letterStates) {
                for (const ll of lll) {
                    if (ll.order !== -1 && ll.order !== -2) {
                        ll.order = -2;
                    }
                    if (ll.order !== -2) {
                        won = false;
                    }
                }
            }
            this.order = 0;
            if (won) {
                clearInterval(this.gameTimer);
                this.roundReady = true;
            }
        } else {
            this.showMessage(`Not in word list`);
        }
    }
    private nextRound() {
        const round = {
            roundNumber: this.roundNumber,
            solutionWords: this.solutionWords,
            status: 'complete',
            startTime: this.timeBegan,
            endTime: this.timeEnd,
            time: this.time,
        };
        this.rounds.push(round);
        this.roundNumber = this.roundNumber + 1;
        this.roundPause = true;
        this.solutionWords = [];

    }
    private removeSolution(sol: SolutionLetter[], index: number) {
        for (const sl of sol) {
            console.log('in remove');
            this.letterStates[sl.y][sl.x].order = -1;
        }
        if (index === -1) {
            this.solution = [];
        } else {
            this.solutionWords.splice(index, 1);
        }
    }
    private getStatus(order: number): string {
        if (order === -1) {
            return 'absent';
        } else if (order === -2) {
            return 'correct';
        } else {
            return 'present';
        }
    }

    private startGame() {
        this.loadRound();
        this.roundPause = false;
        this.gameStarted = true;
        this.timeBegan = new Date();
        this.gameTimer = setInterval(this.clockRunning, 10);
    }
    private gameText() {
        let text: string = '';
        if (this.roundNumber === 1) {
            text = 'Lemons is an anagram game where you can play for the best time or the best score.\n';
            text = text + '3- and 4- letter words are 1 point each\n' +
                   '5-letter words are 2 points each\n' +
                   '6-letter words are 3 points each\n' +
                   '7-letter words are 5 points each\n' +
                   '8-letter words are 11 points each';
        } else if (this.roundNumber === 2) {
            text = 'some score thing';
        } else if (this.roundNumber === 3) {
            text = 'another score';
        }
        return text;
    }
    private shareGame() {
        let totalScore: number = 0;
        let hour: number = 0;
        let min: number = 0;
        let sec: number = 0;
        let ms: number = 0;

        for (const round of this.rounds) {
            totalScore = totalScore + this.score(round);
            const timeElapsed = new Date(round.endTime.getTime() - round.startTime.getTime());
            hour += timeElapsed.getUTCHours();
            min += timeElapsed.getUTCMinutes();
            sec += timeElapsed.getUTCSeconds();
            ms += timeElapsed.getUTCMilliseconds();
        }

        const totalTime =
            this.zeroPrefix(hour, 2) + ':' +
            this.zeroPrefix(min, 2) + ':' +
            this.zeroPrefix(sec, 2) + '.' +
            this.zeroPrefix(ms, 3);

        const shareText: string = '🍋 Lemons 🍋\n' + 'Time: ' + totalTime + '\n' + 'Score: ' + totalScore;
        if (navigator.share) {
            navigator.share({
                text: shareText,
            }).then(() => {
                console.log('Thanks for sharing!');
            }).catch(console.error);
        } else {
            navigator.clipboard.writeText(shareText);
        }
    }
    private clockRunning() {
        this.timeEnd = new Date();
        const timeElapsed = new Date(this.timeEnd.getTime() - this.timeBegan.getTime() - this.stoppedDuration);
        const hour = timeElapsed.getUTCHours();
        const min = timeElapsed.getUTCMinutes();
        const sec = timeElapsed.getUTCSeconds();
        const ms = timeElapsed.getUTCMilliseconds();

        this.time =
            this.zeroPrefix(hour, 2) + ':' +
            this.zeroPrefix(min, 2) + ':' +
            this.zeroPrefix(sec, 2) + '.' +
            this.zeroPrefix(ms, 3);
    }

    private zeroPrefix(num, digit) {
        let zero = '';
        for (let i = 0; i < digit; i++) {
            zero += '0';
        }
        return (zero + num).slice(-digit);
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
.overlay {
    position: fixed;
    z-index: 9998;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, .5);
}

.modal {
    --height: min(350px, calc(var(--vh, 100vh) - 310px));
    height: 500px;
    width: 500px;
    padding: 20px 30px;
    background-color: #fff;
}

.close{
    position: absolute;
    top: 10px;
    right: 10px;
}
@media (max-height: 680px) {
    .tile {
        font-size: 3vh;
    }
}
/* CSS */
.button-1 {
    background-color: #fcc219;
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

/* .button-1:hover {
   background-color: #ffebca;
   } */
.button-2 {
    background-color: #fcc219;
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
    line-height: 20px;
    list-style: none;
    margin: 3px;
    outline: none;
    position: relative;
    text-align: center;
    text-decoration: none;
    transition: color 100ms;
    vertical-align: baseline;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}
.button-3 {
    background-color: #f8932b;
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
    line-height: 20px;
    list-style: none;
    margin: 3px;
    outline: none;
    position: relative;
    text-align: center;
    text-decoration: none;
    transition: color 100ms;
    vertical-align: baseline;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}
.button-4 {
    background-color: #75803e;
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
    line-height: 20px;
    list-style: none;
    margin: 3px;
    outline: none;
    position: relative;
    text-align: center;
    text-decoration: none;
    transition: color 100ms;
    vertical-align: baseline;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
}

/* .button-2:hover,
   .button-2:focus {
   background-color: #ffebca;
   } */
</style>
