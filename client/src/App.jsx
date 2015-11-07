import React from 'react';

import {Modal} from './components';
import {FriendsView, BrewingView} from './views';
import * as api from './api';
import {Inventory} from './data';
import {find} from 'lodash';

export default class App extends React.Component {
	constructor() {
		super();

		this.types = null;

		this.state = {
			...this.state,
			gameState: null,
			stage: new Inventory(),
			inventory: new Inventory(),
			tick: 0,
			friendsOpen: false,
		};
	}

	static childContextTypes = {
		dispatch: React.PropTypes.func,
		types: React.PropTypes.object,
		tick: React.PropTypes.number,
	};

	componentWillUpdate(props, state) {
		const {gameState, stage} = state;

		// calculate inventory
		if (gameState && gameState.inventory && stage) {
			const inventory = new Inventory(gameState.inventory);

			const stageChanged = !this.state.stage || !stage.equals(this.state.stage);
			const inventoryChanged = !this.state.gameState || !this.state.gameState.inventory ||
				!inventory.equals(new Inventory(this.state.gameState.inventory));

			if (stageChanged || inventoryChanged) {
				this.setState({
					inventory: inventory.subtract(stage)
				});
			}
		}
	}

	getChildContext() {
		return {
			dispatch: ::this.dispatch,
			types: this.types,
			tick: this.state.tick,
		};
	}

	async dispatch(action) {
		const {type} = action;

		if (type === 'stage.confirm') {
			await this::this.confirmStage();
		} else if (type === 'stage.clear') {
			this.setState({
				stage: new Inventory()
			});
		} else if (type === 'stage.add') {
			this.setState({
				stage: this.state.stage.add(new Inventory({[action.item_type_id]: action.count}))
			});
		} else if (type === 'stage.remove') {
			this.setState({
				stage: this.state.stage.subtract(new Inventory({[action.item_type_id]: action.count}))
			});
		} else if (type === 'collect') {
			await api.postCollectAction();
			await this::this.updateGameState();
		} else if (type === 'reload') {
			await this::this.updateGameState();
		} else if (type === 'reload.full') {
			await Promise.all([
				this::this.updateGameState(),
				this::this.updateTypes(),
			]);
		} else if (type === 'friends.toggle') {
			await this::this.toggleFriendsOverlay();
		} else if (type === 'friends.add') {
			await this::this.addFriend(action.username);
		} else {
			console.warn(`Unhandled action type: ${type}`);
		}
	}

	async addFriend(username) {
		await api.postAddFriend(username);
	}

	async confirmStage() {
		// find the recipe
		const {stage} = this.state;
		const {recipes} = this.types;
		const recipe = find(recipes, (recipe) => stage.equals(new Inventory(recipe.recipe_items)));

		if (recipe) {
			await api.postBrewAction(recipe.id);
			::this.updateGameState();
			this.setState({
				stage: new Inventory()
			});
		} else {
			console.log('Recipe not found.');
		}

	}

	componentWillMount() {
		::this.updateGameState();
		::this.updateTypes();
	}

	componentDidMount() {
		this._interval = setInterval(::this.tick, 400);
		this._interval2 = setInterval(::this.tick2, 4000);
	}

	componentWillUnmount() {
		if (this._interval) {
			clearInterval(this._interval);
		}
		if (this._interval2) {
			clearInterval(this._interval2);
		}
	}

	tick() {
		const tick = this.state.tick + 0.4;
		this.setState({tick});

		if (this.state.gameState) {
			// reload if some item in the queue is done
			if (this.state.gameState.actions.some((action) => {
				return action.end <= tick;
			})) {
				::this.dispatch({
					type: 'reload'
				});
			}
		}
	}

	tick2() {
		::this.updateGameState();
	}

	async updateGameState() {
		let gameState = await api.getGameState();
		this.setState({ gameState, tick: gameState.tick })
	}

	async updateTypes() {
		let types = await api.getTypes();
		this.types = types;
		this.forceUpdate();
	}

	toggleFriendsOverlay() {
		this.setState({ friendsOpen: !this.state.friendsOpen });
	}

	render() {
		if (!this.types || !this.state.gameState) {
			return <div>Loading...</div>;
		}

		const {stage, inventory, gameState, friendsOpen} = this.state;

		return <div className="app">
			<BrewingView stage={stage} inventory={inventory} units={gameState.units} actions={gameState.actions} />

			<Modal open={friendsOpen} onToggle={::this.toggleFriendsOverlay}>
				<FriendsView />
			</Modal>

			<div className="account">
				<a href="/logout">Logout</a>
			</div>
		</div>;
	}
}
