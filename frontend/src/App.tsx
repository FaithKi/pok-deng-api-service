import { useState, useRef, useEffect } from "react";
import "./App.css";

type Card = {
  rank: string;
  suit: string;
  value: Number;
};

type GameState = {
  game_id: string;
  state: string;
  balance: Number;
  player_hand: Card[];
  dealer_hand_visible: Card[];
  player_score: Number;
  dealer_score: Number;
  winner: string;
};

function App() {
  const [gameState, setGameState] = useState<GameState>();
  const balanceRef = useRef<HTMLInputElement>(null);
  const cutAmountRef = useRef<HTMLInputElement>(null);
  const betAmountRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    console.log("gamestate", gameState);
  }, [gameState]);

  const onStartGame = async () => {
    if (balanceRef.current && Number(balanceRef.current.value) > 0) {
      const data = await fetch("http://localhost:8000/game/start", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          balance: balanceRef.current.value,
        }),
      }).then((resp) => resp.json());
      setGameState(data);
      console.log("data", data);
    } else {
      alert("Invalid Initial Balance");
    }
  };

  const onCut = async () => {
    if (
      gameState &&
      cutAmountRef.current &&
      Number(cutAmountRef.current.value) > 0 &&
      Number(cutAmountRef.current.value) < 52
    ) {
      const data = await fetch(
        `http://localhost:8000/game/${gameState.game_id}/action`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            action: "cut",
            amount: cutAmountRef.current.value,
          }),
        },
      ).then((resp) => resp.json());
      setGameState(data);
      console.log("data", data);
    } else {
      alert("No game or Invalid Cut Amount");
    }
  };

  const onBet = async () => {
    if (
      gameState &&
      betAmountRef.current &&
      Number(betAmountRef.current.value) > 0 &&
      Number(betAmountRef.current.value) < Number(gameState.balance)
    ) {
      const data = await fetch(
        `http://localhost:8000/game/${gameState.game_id}/action`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            action: "bet",
            amount: betAmountRef.current.value,
          }),
        },
      ).then((resp) => resp.json());
      setGameState(data);
      console.log("data", data);
    } else {
      alert("No game or Invalid Cut Amount");
    }
  };

  const onDraw = async () => {
    if (gameState) {
      const data = await fetch(
        `http://localhost:8000/game/${gameState.game_id}/action`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            action: "draw",
          }),
        },
      ).then((resp) => resp.json());
      setGameState(data);
      console.log("data", data);
    } else {
      alert("No game");
    }
  };

  const onStay = async () => {
    if (gameState) {
      const data = await fetch(
        `http://localhost:8000/game/${gameState.game_id}/action`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            action: "draw",
          }),
        },
      ).then((resp) => resp.json());
      setGameState(data);
      console.log("data", data);
    } else {
      alert("No game");
    }
  };

  return (
    <>
      <div>
        <span>Set Initial Balance</span>
        <input type="number" ref={balanceRef}></input>
        <button onClick={onStartGame}>New Game</button>
      </div>
      <div>
        {gameState ? (
          <>
            <span>State</span>
            <span>{gameState.state}</span>
            <span>Player's hand</span>
            <span>
              {gameState.player_hand.map((card) => (
                <div>
                  <div>
                    <span>rank</span>
                    <span>{card.rank}</span>
                  </div>
                  <div>
                    <span>suit</span>
                    <span>{card.suit}</span>
                  </div>
                </div>
              ))}
            </span>
            <span>Player's score</span>
            <span>{String(gameState.player_score)}</span>
            <span>Dealer's hand</span>
            <span>
              {gameState.dealer_hand_visible.map((card) => (
                <div>
                  <div>
                    <span>rank</span>
                    <span>{card.rank}</span>
                  </div>
                  <div>
                    <span>suit</span>
                    <span>{card.suit}</span>
                  </div>
                </div>
              ))}
            </span>
            <span>Dealer's score</span>
            <span>{String(gameState.dealer_score)}</span>
            <span>Game Result</span>
            <span>
              {gameState.winner == "Player"
                ? "You Win"
                : gameState.winner == "Dealer"
                  ? "You Lose"
                  : "Draw"}
            </span>
          </>
        ) : (
          <div>No Game</div>
        )}
      </div>
      <div>
        <input ref={cutAmountRef}></input>
        <button onClick={onCut}>Cut</button>
        <input ref={betAmountRef}></input>
        <button onClick={onBet}>Bet</button>
        <button onClick={onDraw}>Draw</button>
        <button onClick={onStay}>Stay</button>
      </div>
    </>
  );
}

export default App;
