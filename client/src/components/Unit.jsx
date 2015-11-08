import React from 'react';
import {BaseComponent} from '../BaseComponent';
import Sprite from './Sprite';
import {find} from '../data';

import * as unitSprites from '../resources/units';

export default class Unit extends BaseComponent {
	static contextTypes = {
		types: React.PropTypes.object.isRequired,
	}

	render() {
		const {height, unit_type_id} = this.props;

		const unitType = find(this.context.types.unit_types, unit_type_id);
		const sprite = unitSprites[unitType.image];

		return <Sprite {...sprite} displayHeight={height} displayUnit='vw' />;
	}
}
