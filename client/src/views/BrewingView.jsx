import React from 'react';

import {Queue, Sprite, Cauldron, Shelf, Stage} from '../components';
import {Inventory, find} from '../data';

import * as unitSprites from '../resources/units';

export default class BrewingView extends React.Component {
	static contextTypes = {
		types: React.PropTypes.object.isRequired,
	}

	render() {
		const {
			stage,
			inventory,
			units,
			actions,
		} = this.props;

		const arr = inventory.toArray();
		const inventoryLeft = new Inventory(arr.slice(0, 12));
		const inventoryRight = new Inventory(arr.slice(12));

		return <div className="brewing-view">
			<div className="units">
				{ units && units.map((unit) => {
					const unitType = find(this.context.types.unit_types, unit.unit_type_id);
					const sprite = unitSprites[unitType.image];
					return <Sprite {...sprite} key={unit.id} displayHeight={12} displayUnit='vw' />;
				})}

			</div>

			<Shelf inventory={inventoryLeft} className="left" />
			<Shelf inventory={inventoryRight} className="right" />

			<Cauldron />

			<Stage items={stage} />

			<Queue actions={actions} />
		</div>;
	}
}
