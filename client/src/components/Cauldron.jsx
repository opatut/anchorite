import React from 'react';
import {BaseComponent} from '../BaseComponent';

import {Sprite} from '../components';

import {base, brew} from '../resources/cauldron';

export default class Cauldron extends BaseComponent {
	render() {
		const {brewing} = this.props;
		return <div className='cauldron'>
			<Sprite {...base} displayHeight={16} displayUnit='vw' className='base' />
			{brewing && <Sprite {...brew} displayHeight={16} displayUnit='vw' className='brew' />}
		</div>;
	}
}
