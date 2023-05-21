import React, { useState, useEffect } from 'react';
import { View, TouchableOpacity, StyleSheet, Text, Animated } from 'react-native';
import Ionicons from 'react-native-vector-icons/Ionicons';
import MaterialIcons from 'react-native-vector-icons/MaterialIcons';
import Entypo from 'react-native-vector-icons/Entypo';
import { useNavigation, useRoute } from '@react-navigation/native';
import { useCookies } from 'react-cookie';

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    height: 60,
    backgroundColor: '#3180e7',
    borderTopLeftRadius: 30,
    borderTopRightRadius: 30,
    borderBottomRightRadius: 0,
    borderBottomLeftRadius: 0,
  },
  icon: {
    marginBottom: 4,
  },
  activeIcon: {
    height: 65,
    width: 65,
    marginBottom: 55,
    fontSize: 40,
    borderWidth: 3,
    borderColor: '#3180e7',
    borderRadius: 100,
    padding: 10,
    color: '#3180e7',
    backgroundColor: 'white',
    shadowColor: 'black',
    shadowOffset: {
      width: 0,
      height: 5,
    },
    shadowOpacity: 0.3,
    shadowRadius: 15,
    elevation: 5,
    justifyContent: 'center',
    alignItems: 'center',
  },
  
  dropdownContainer: {
    position: 'absolute',
    bottom: 60,
    right: 0,
    backgroundColor: '#3180e7',
    padding: 10,
    zIndex: 999,
    borderTopLeftRadius: 0,
    borderTopRightRadius: 40,
    borderBottomRightRadius: 0,
    borderBottomLeftRadius: 40,
    marginBottom: 2,
    marginRight: 15,
    
  },
  dropdownItem: {
    color: 'white',
    fontSize: 16,
    padding: 8,
    fontWeight: 'bold',
  },
});

const BottomNavBar = ({ cartList, cartItems }) => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [isNewMessageIconBigger, setIsNewMessageIconBigger] = useState(false);
  const [animation] = useState(new Animated.Value(0));

  const [token, setToken, removeToken] = useCookies(['myToken']);
  const [group, setGroup, removeGroup] = useCookies(['myGroup']);

  const navigation = useNavigation();
  const route = useRoute();

  useEffect(() => {
    if (route.name === 'Services') {
      setIsNewMessageIconBigger(true);
      
    } else {
      setIsNewMessageIconBigger(false);
      
    }
  }, [route.name, animation]);

  const toggleDropdown = () => {
    setIsDropdownOpen((prevState) => !prevState);
  };

  const handleLogout = () => {
    removeToken('access_token');
    removeGroup('group');

    console.log('Logged out successfully');

    navigation.navigate('Login');
  };

  

  return (
    <View>
      <View style={styles.container}>
        <TouchableOpacity onPress={() => navigation.navigate('Home')}>
          <Ionicons name="home" size={25} color="white" style={styles.icon} />
        </TouchableOpacity>
        <TouchableOpacity>
          <MaterialIcons name="history-edu" size={25} color="white" style={styles.icon} />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => navigation.navigate('Appointment', { cartList, cartItems })}>
          <Entypo
            name="new-message"
            size={isNewMessageIconBigger ? 30 : 25}
            color="white"
            style={[styles.icon, isNewMessageIconBigger && styles.activeIcon]}
          />
        </TouchableOpacity>
        <TouchableOpacity onPress={() => navigation.navigate('Services')}>
          <MaterialIcons name="medical-services" size={25} color="white" style={styles.icon} />
        </TouchableOpacity>
        <TouchableOpacity onPress={toggleDropdown}>
          <Ionicons name="settings" size={25} color="white" style={styles.icon} />
        </TouchableOpacity>
      </View>

      {isDropdownOpen && (
        <View style={styles.dropdownContainer}>
          <TouchableOpacity
            onPress={() => {
              navigation.navigate('Profile');
              setIsDropdownOpen((prevState) => !prevState);
            }}
          >
            <Text style={styles.dropdownItem}>Profile</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={handleLogout}>
            <Text style={styles.dropdownItem}>Logout</Text>
          </TouchableOpacity>
        </View>
      )}
    </View>
  );
};

export default BottomNavBar;
