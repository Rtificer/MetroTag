import React, { useState } from 'react';
import { Text, StyleSheet, View, Button, TextInput } from 'react-native';
import { useNavigation } from '@react-navigation/native';

export default function HomeScreen() {
	const [name, setName] = useState('');
	const [submitted, setSubmitted] = useState(false);
	const navigation = useNavigation();

	const handleSubmit = () => {
		setSubmitted(true);
	};

	const handleRoleSelection = (role: string) => {
		navigation.navigate(role === 'tagger' ? 'tagger' : 'runner', { name });
	};

	return (
		<View style={styles.container}>
			{!submitted ? (
				<>
					<Text>What is your Username?</Text>
					<TextInput
						style={styles.input}
						value={name}
						onChangeText={setName}
						placeholder="Enter your username"
					/>
					<Button title="Submit" onPress={handleSubmit} />
				</>
			) : (
				<>
					<Text>Hello, {name}! Are you a tagger or a runner?</Text>
					<Button
						title="Tagger"
						onPress={() => handleRoleSelection('tagger')}
					/>
					<Button
						title="Runner"
						onPress={() => handleRoleSelection('runner')}
					/>
				</>
			)}
		</View>
	);
}

const styles = StyleSheet.create({
	container: {
		flex: 1,
		justifyContent: 'center',
		alignItems: 'center',
		padding: 16
	},
	input: {
		height: 40,
		borderColor: 'gray',
		borderWidth: 1,
		marginBottom: 12,
		paddingHorizontal: 8,
		width: '80%'
	}
});
