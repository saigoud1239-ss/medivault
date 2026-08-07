import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:uuid/uuid.dart';

import '../models/medicine_model.dart';
import '../providers/medicine_provider.dart';

class AddMedicineScreen extends StatefulWidget {
  const AddMedicineScreen({super.key});

  @override
  State<AddMedicineScreen> createState() => _AddMedicineScreenState();
}

class _AddMedicineScreenState extends State<AddMedicineScreen> {
  final _nameController = TextEditingController();
  final _notesController = TextEditingController();
  MedicineType _selectedType = MedicineType.TABLET;
  FoodRelation _selectedFood = FoodRelation.AFTER_FOOD;
  bool _morningSlot = true;
  bool _nightSlot = true;

  void _saveMedicine() {
    if (_nameController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please enter Medicine Name')),
      );
      return;
    }

    final newMed = MedicineModel(
      id: const Uuid().v4(),
      userId: "usr-patient-892401",
      medicineName: _nameController.text,
      type: _selectedType,
      foodRelation: _selectedFood,
      startDate: DateTime.now().toString().split(' ')[0],
      endDate: DateTime.now().add(const Duration(days: 30)).toString().split(' ')[0],
      notes: _notesController.text,
      schedules: [
        if (_morningSlot) MedicineSchedule(id: const Uuid().v4(), slot: DoseSlot.MORNING, time: "08:00", dosage: "1 Dose"),
        if (_nightSlot) MedicineSchedule(id: const Uuid().v4(), slot: DoseSlot.NIGHT, time: "22:00", dosage: "1 Dose"),
      ],
    );

    Provider.of<MedicineProvider>(context, listen: false).addMedicine(newMed);
    Navigator.pop(context);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('✔ Added ${_nameController.text} to Schedule')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Add New Medication')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAlignment.start,
          children: [
            TextField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: 'Medicine Name *',
                hintText: 'e.g. Aspirin 100mg',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),

            Row(
              children: [
                Expanded(
                  child: DropdownButtonFormField<MedicineType>(
                    value: _selectedType,
                    decoration: const InputDecoration(labelText: 'Type', border: OutlineInputBorder()),
                    items: MedicineType.values.map((t) {
                      return DropdownMenuItem(value: t, child: Text(t.name));
                    }).toList(),
                    onChanged: (val) => setState(() => _selectedType = val!),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: DropdownButtonFormField<FoodRelation>(
                    value: _selectedFood,
                    decoration: const InputDecoration(labelText: 'Food Relation', border: OutlineInputBorder()),
                    items: FoodRelation.values.map((f) {
                      return DropdownMenuItem(value: f, child: Text(f.name.replaceAll('_', ' ')));
                    }).toList(),
                    onChanged: (val) => setState(() => _selectedFood = val!),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),

            const Text('Dosage Slots', style: TextStyle(fontWeight: FontWeight.w700)),
            CheckboxListTile(
              title: const Text('Morning 🌅 (8:00 AM)'),
              value: _morningSlot,
              onChanged: (val) => setState(() => _morningSlot = val!),
            ),
            CheckboxListTile(
              title: const Text('Night 🌙 (10:00 PM)'),
              value: _nightSlot,
              onChanged: (val) => setState(() => _nightSlot = val!),
            ),
            const SizedBox(height: 16),

            TextField(
              controller: _notesController,
              decoration: const InputDecoration(
                labelText: 'Notes / Special Instructions',
                hintText: 'e.g. Take with warm water after breakfast',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),

            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _saveMedicine,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: const Color(0xFF0284C7),
                  foregroundColor: Colors.white,
                ),
                child: const Text('Save Medication', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
