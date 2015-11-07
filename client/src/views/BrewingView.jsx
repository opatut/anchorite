import React from 'react';

import {Cauldron, Shelf, Stage} from '../components';
import {Inventory} from '../data';

export default class BrewingView extends React.Component {
	render() {
		const {
			stage,
			inventory,
		} = this.props;

		const arr = inventory.toArray();
		const inventoryLeft = new Inventory(arr.slice(0, 12));
		const inventoryRight = new Inventory(arr.slice(12));

		return <div className="brewing-view">
			<div>
				<Stage items={stage} />
			</div>
			<div>
				<Shelf inventory={inventoryLeft} />
				<Cauldron />
				<Shelf inventory={inventoryRight} />
			</div>
			<div>
				Queue
			</div>
		</div>;
	}
}
