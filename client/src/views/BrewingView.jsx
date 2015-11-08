import React from 'react';
import {BaseComponent} from '../BaseComponent';

import {Chat, Unit, Queue, Sprite, Cauldron, Shelf, Stage} from '../components';
import {Inventory, find} from '../data';

export default class BrewingView extends BaseComponent {
	static contextTypes = {
		types: React.PropTypes.object.isRequired,
		dispatch: React.PropTypes.func.isRequired,
	}

	render() {
		const {dispatch} = this.context;

		const {
			stage,
			inventory,
			units,
			actions,
			messages,
		} = this.props;

		const arr = inventory.toArray();
		const inventoryLeft = new Inventory(arr.slice(0, 12));
		const inventoryRight = new Inventory(arr.slice(12));

		const brewing = actions.length ? actions[0].type === 'brew_action' : false;

		return <div className="brewing-view">
			<div className="units">
				{ units && units.map((unit) => <Unit {...unit} height={12} key={unit.id} />) }
			</div>

			<Stage items={stage} />

			<Shelf inventory={inventoryLeft} className="left" />
			<Shelf inventory={inventoryRight} className="right" />

			<div className="center">
				<Cauldron {...{brewing}} />
			</div>

			<div className="bottom">
				<div className="left">
					<Chat messages={messages} />
				</div>
				<div className="right">
					<Queue actions={actions} />
					<div className="actions">
						<button className="button" onClick={() => dispatch({ type: 'friends.toggle' })}>Neighbors</button>
						<button className="button" onClick={() => dispatch({ type: 'attacks.toggle' })}>Fights</button>
						<button className="button" onClick={() => dispatch({ type: 'collect' })}>Collect herbs</button>
					</div>
				</div>
			</div>
		</div>;
	}
}
