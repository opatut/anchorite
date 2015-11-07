import React from 'react';

import {BrewingView} from './views';
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
		switch (action.type) {
			case 'stage.confirm':
				::this.confirmStage();
				break;

			case 'stage.clear':
				this.setState({
					stage: new Inventory()
				});
				break;

			case 'stage.add':
				this.setState({
					stage: this.state.stage.add(new Inventory({[action.item_type_id]: action.count}))
				});
				break;

			case 'stage.remove':
				this.setState({
					stage: this.state.stage.subtract(new Inventory({[action.item_type_id]: action.count}))
				});
				break;

			case 'reload':
				::this.updateGameState();
				break;

			default:
				console.warn(`Unhandled action type: ${action.type}`);
		}
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
	}

	componentWillUnmount() {
		if (this._interval) {
			clearInterval(this._interval);
		}
	}

	tick() {
		const tick = this.state.tick + 0.4;
		this.setState({tick});

		if (this.state.gameState) {
			// reload if some item in the queue is done
			if (this.state.gameState.actions.some((action) => {
				return action.tick <= tick;
			})) {
				::this.dispatch({
					type: 'reload'
				});
			}
		}
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

	/*
	 * Stage management
	 */

	render() {
		if (!this.types || !this.state.gameState) {
			return <div>Loading...</div>;
		}

		const {stage, inventory, gameState} = this.state;

		return <div className="app">
			<BrewingView stage={stage} inventory={inventory} units={gameState.units} actions={gameState.actions} />
			<div className="account">
				<a href="/logout">Logout</a>
			</div>
		</div>;
	}
}
