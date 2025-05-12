// Switch to my_data database
db = db.getSiblingDB("my_data");

// Import will be handled by mongoimport, but we can create indexes and initial data

// Create indexes for better performance
db.open_data.createIndex({ name: 1 });
db.open_data.createIndex({ class: 1 });
db.open_data.createIndex({ level: -1 });
db.open_data.createIndex({ rank: 1 });
db.open_data.createIndex({ ladder: 1 });

// Create my_team collection with initial data
db.my_team.insertMany([
  {
    name: "Team Member 1",
    role: "Database Administrator",
    email: "admin@lab165.local",
    specialization: "MongoDB Management",
    created_at: new Date(),
  },
  {
    name: "Team Member 2",
    role: "Application Developer",
    email: "dev@lab165.local",
    specialization: "Flask Applications",
    created_at: new Date(),
  },
  {
    name: "Team Member 3",
    role: "Data Analyst",
    email: "analyst@lab165.local",
    specialization: "Data Visualization",
    created_at: new Date(),
  },
]);

print("MongoDB initialization completed successfully!");
print("Created indexes on open_data collection");
print("Created my_team collection with team members");
