import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { useCookies } from 'react-cookie';

const ResultCards = () => {
  const [results, setResults] = useState([]);
  const [token] = useCookies(['myToken']);

  useEffect(() => {
    fetchResults();
  }, []);

  const fetchResults = async () => {
    try {
      // Fetch test results
      const response = await fetch('http://192.168.0.106:8000/api/main/test-results/', {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token.access_token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch results');
      }

      const data = await response.json();

      const resultData = await Promise.all(
        data.map(async (result) => {
          // Fetch related sample data
          const sampleResponse = await fetch(`http://192.168.0.106:8000/api/main/medical-samples/${result.medical_sample}/`, {
            method: 'GET',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token.access_token}`,
            },
          });

          if (!sampleResponse.ok) {
            throw new Error('Failed to fetch sample data');
          }

          const sampleData = await sampleResponse.json();

          // Fetch related appointment data
          const appointmentResponse = await fetch(`http://192.168.0.106:8000/api/main/appointments/${sampleData.appointment}/`, {
            method: 'GET',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token.access_token}`,
            },
          });

          if (!appointmentResponse.ok) {
            throw new Error('Failed to fetch appointment data');
          }

          const appointmentData = await appointmentResponse.json();

          // Fetch related services data
          const serviceResponse = await fetch(`http://192.168.0.106:8000/api/main/services/${appointmentData.service}/`, {
            method: 'GET',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token.access_token}`,
            },
          });

          if (!serviceResponse.ok) {
            throw new Error('Failed to fetch services data');
          }

          const servicesData = await serviceResponse.json();
          const serviceNames = servicesData.services.map(service => service.test_name);

          return {
            ...result,
            serviceNames,
            collection_date: sampleData.collection_date,
            collection_time: sampleData.collection_time,
          };
        })
      );

      setResults(resultData);
    } catch (error) {
      console.error(error);
    }
  };

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <View style={styles.cardHeader}>
        <Text style={styles.title}>Test Result:</Text>
        <Text style={styles.subtitle}>{item.medical_sample.sample_type}</Text>
      </View>
      <View style={styles.serviceContainer}>
        <Text style={styles.serviceTitle}>Services:</Text>
        {item.serviceNames.map((serviceName, index) => (
          <Text key={index} style={styles.serviceName}>
            {`${index + 1}. ${serviceName}`}
          </Text>
        ))}
      </View>
      <Text style={styles.collectionDateTime}>
        Collection Date: {item.collection_date}, Collection Time: {item.collection_time}
      </Text>
      <Text style={styles.result}>{item.result}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={results}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
  },
  listContainer: {
    paddingBottom: 20,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
    elevation: 2,
  },
  cardHeader: {
    backgroundColor: '#eaeaea',
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  subtitle: {
    fontSize: 16,
  },
  serviceContainer: {
    backgroundColor: '#f5f5f5',
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
  serviceTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  serviceName: {
    fontSize: 14,
    marginBottom: 2,
    marginLeft: 20,
  },
  collectionDateTime: {
    fontSize: 12,
    marginBottom: 10,
  },
  result: {
    fontSize: 14,
  },
});

export default ResultCards;
